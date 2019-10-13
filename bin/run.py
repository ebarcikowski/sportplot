"""
Toy mostly for running interactively to see what things are doing.
"""
from sportplot.gpx_parser import GPXFile
from sportplot.postprocess import ActData
from sportplot import analysis as anal
import altair as alt
import panel as pn

alt.renderers.enable('default')
pn.extension('vega')

sample_file = '/home/elliottb/garmin/4132209152_activity.gpx'
gpx = GPXFile(sample_file)

act_data = ActData(gpx.points)

time_in_zone = anal.get_time_in_zone(act_data.df, 160)

zones = alt.Chart(time_in_zone).mark_bar().encode(
    x='zone',
    y='time'
)

base = alt.Chart(act_data.df).encode(
    x='time'
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
        # scale=alt.Scale(zero=False)
    ),
).interactive()

multi = alt.vconcat(
    ele,
    hr,
)

dashboard = pn.Column()
dashboard.append(pn.Row(ele))
dashboard.append(pn.Row(hr))
dashboard.append(pn.Row(zones))

dashboard.servable()
