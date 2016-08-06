from flask import Flask, request, redirect, render_template, send_file
import os
import pandas as pd
from call_apis import call_watson, parse_response, get_tweets, format_tweets


def create_app():
    app=Flask(__name__)
    return app

app = create_app()

def get_watson_tweets(username):
    statuses = get_tweets(username)
    mydf = format_tweets(statuses)
    response = call_watson(mydf)
    cognitive_df = parse_response(response)
    return cognitive_df
    
def get_compare_data(username_one, username_two):
    ye_df = get_watson_tweets(username_one)
    tyga_df = get_watson_tweets(username_two)
    ye_sm = ye_df[['name', 'percentile']]
    ty_sm = tyga_df[['name', 'percentile']]
    suffixes = ('_' + username_one, '_' + username_two)
    my_df = pd.merge(ye_sm, ty_sm, on="name", suffixes=suffixes)
    my_df.columns = ['category', username_one, username_two]
    return my_df


@app.route('/', methods = ['GET','POST'])
def signup():
    index = 'index.html'
    if request.method == 'POST':
        if request.form['btn'] == 'display':
            unames_lst = request.form.getlist('celeb')
            my_df = get_compare_data(unames_lst[0], unames_lst[1])
            return render_template(index, flat=my_df.to_html(index=False))
        if request.form['btn'] == 'download':
            unames_lst = request.form.getlist('celeb')
            my_df = get_compare_data(unames_lst[0], unames_lst[1])
            xls_name = "Watson_Results.xlsx"
            df_xls = my_df.to_excel(xls_name, index=False)
            return send_file(xls_name, as_attachment=True)
        if request.form['btn'] == 'graph':
            unames_lst = request.form.getlist('celeb')
            my_df = get_compare_data(unames_lst[0], unames_lst[1])
            chart = {"renderTo": 'chart_ID', "type": 'bar', "height": 350}
            series = [{"name": str(unames_lst[0]), "data": my_df[unames_lst[0]].tolist()}, {"name": str(unames_lst[1]), "data": my_df[unames_lst[1]].tolist()}]
            title = {"text": 'Watson Results'}
            print my_df['category'].tolist()
            foo = my_df['category'].tolist()
            bar = [str(x) for x in foo]
            xAxis = {"categories": bar}
            print xAxis
            yAxis = {"title": {"text": 'Percentile Ranks'}}
            return render_template(index, chartID='chart_ID', chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

    return render_template(index)

	
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=int(port), debug=True)
