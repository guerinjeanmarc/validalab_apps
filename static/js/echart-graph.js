var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

var nodesForGraph=graph.nodes.map(v=>({...v,symbolSize:v.size*10,category:v.Community
}))
var linksForGraph=graph.links.map(v=>({...v,source:v.source.id,target:v.target.id
}))
console.log(linksForGraph)
var communities=[
      {
        "name": "-1"
      },
      {
        "name": "-0.5"
      },
      {
        "name": "1"
      },
      {
        "name": "None"
      }
    ]
myChart.showLoading();

myChart.hideLoading();
option = {
        title: {
            text: 'Les medias',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
        },
        tooltip: {},
        legend: [{
            // selectedMode: 'single',
            data: communities.map(function (a) {
                return a.name;
            })
        }],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                name: 'Media Français',
                type: 'graph',
                layout: 'force',
                data: nodesForGraph,
                links: linksForGraph,
                categories: communities,
                roam: true,
                draggable:true,
                itemStyle:{
                  borderColor:'#fff',
                  borderWidth:1,
                  borderTYpe:'solid'
                },
                label: {
                  show:true,
                    position: 'inside',
                    formatter: '{b}',
                    fontWeight:'bolder',
                    color:'#fff'
                },
                labelLayout: {
                    hideOverlap: true
                },
                force: {
                edgeLength: 10,
                repulsion: [10,200],
                gravity: 0.1
            },
                lineStyle: {
                    color: 'source',
                    curveness: 0,
                    width:3
                },
                edgeSymbolSize:[10,40],
                emphasis: {
                    focus: 'adjacency',
                    lineStyle: {
                        width: 20
                    },
                    label: {
                    position: 'right',
                    show: true
                }
                }
            }
        ]
    };
    var zr = myChart.getZr();
    myChart.setOption(option);

    

 
    myChart.on('click', function (params) {
showDetails(params.data.name+"Website")
get_info(params.data.name)
	});