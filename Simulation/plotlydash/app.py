import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Dash 앱 초기화
app = dash.Dash(__name__)

# 레이아웃 설정
app.layout = html.Div([
    dcc.Graph(id='line-chart'),
    
    html.Label('시작 연령'),
    dcc.Slider(
        id='x-start-slider',
        min=18,
        max=31,
        step=1,
        marks={i: str(i) for i in range(11)},
        value=1
    ),
    
    html.Label('은퇴 연령'),
    dcc.Slider(
        id='x-end-slider',
        min=64,
        max=80,
        step=1,
        marks={i: str(i) for i in range(11)},
        value=1
    ),
    
    html.Label('데이터'),
    dcc.Slider(
        id='xy-slider',
        min=0,
        max=5,
        step=0.1,
        marks={i: str(i) for i in range(11)},
        value=0
    ),
    
    html.Label('리스크 레벨'),
    dcc.Slider(
        id='risk-level-slider',
        min=0.1,
        max=1,
        step=0.1,
        marks={i/10: str(i/10) for i in range(1, 11)},
        value=0.1
    ),
    
    html.Label('추가값'),
    dcc.Slider(
        id='additional-slider',
        min=0,
        max=5,
        step=0.1,
        marks={i: str(i) for i in range(11)},
        value=0
    )
])

# 콜백 함수 생성
@app.callback(
    Output('line-chart', 'figure'),
    [Input('x-start-slider', 'value'), Input('x-end-slider', 'value'), Input('xy-slider', 'value'), Input('risk-level-slider', 'value'), Input('additional-slider', 'value')]
)
def update_chart(x_start_value, x_end_value, xy_value, risk_level_value, additional_value):
    x_values = [x_start_value + i * ((x_end_value - x_start_value) / 100) for i in range(101)]
    y_values = [(xy_value) * (i + 1) * risk_level_value + additional_value for i in range(101)]

    trace = go.Scatter(x=x_values, y=y_values, mode='lines+markers', marker=dict(size=5), fill='tozeroy')
    layout = go.Layout(title=f'Area Chart (X={x_start_value} to X={x_end_value}, Y={xy_value} * Risk Level={risk_level_value} + {additional_value})', xaxis=dict(range=[x_start_value, x_end_value]), yaxis=dict(range=[0, max(y_values)]))
    return {'data': [trace], 'layout': layout}

# 앱 실행
if __name__ == '__main__':
    app.run_server(debug=True)
