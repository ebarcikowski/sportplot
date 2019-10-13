from flask import Flask, render_template
import altair as alt
from sportplot import gpx_parser, analysis, postprocess

app = Flask(__name__)

DEFAULT_GPX = 'data/4132209152_activity.gpx'
gpx = gpx_parser.GPXFile(DEFAULT_GPX)
act_data = postprocess.ActData(gpx.points)


@app.route('/')
def index():
    return render_template('index.html',
                           summary=act_data.get_summary_text())


@app.route('/charts/ele')
def chart_ele():
    base = alt.Chart(act_data.df).encode(
        alt.X('hoursminutesseconds(time_from_start)', title='Time')
    )

    ele = base.mark_line().encode(
        alt.Y(
            'ele',
            axis=alt.Axis(title='Elevation'),
            scale=alt.Scale(zero=False)
        ),
    ).interactive()

    hr = base.mark_line().encode(
        alt.Y(
            'hr',
            axis=alt.Axis(title='Heart Rate')
        ),
    ).interactive()

    multi = alt.vconcat(
        ele,
        hr,
        )
    return multi.to_json()


@app.route('/charts/zones')
def chart_zones():
    time_in_zone = analysis.get_time_in_zone(act_data.df, 160)
    zones = alt.Chart(
        data=time_in_zone,
        # height=700,
        # width=600
    ).mark_bar().encode(
        x='zone',
        y='time'
    ).interactive()
    return zones.to_json()


if __name__ == '__main__':
    app.run(debug=True)
