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
        "name": "Serieux"
      },
      {
        "name": "Droite"
      },
      {
        "name": "Gauche"
      },
      {
        "name": "Complotistes"
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





  var highlight= {
    title: {
        text: 'Les medias',
        subtext: 'Default layout',
        top: 'bottom',
        left: 'right'
    },
    tooltip: {},
    legend: [{
      textStyle: {
        color: "white" ,
        fontWeight:"700",
        fontSize:14
      }            ,
backgroundColor: 'black' ,
/* borderColor:'#fff',
borderWidth:2, */
        //selectedMode: 'single',
        data: communities.map(function (a) {
            return a.name;
        })
    }],
    animationDuration: 1500,
    animationEasingUpdate: 'quinticInOut',
    markPoint:{data:{itemStyle:{
      color: nodesForGraph.map(function (a) {
        return a.color;
    })
    }}

    },
    series: [
        {
            name: 'Media Français',
            type: 'graph',
            layout: 'force',
            data: nodesForGraph.map(function (node) {
              return node.id==toHighlight?{
                  x: node.x,
                  y: node.y,
                  id: node.id,
                  name: node.name,
                  symbolSize: 200,
                  itemStyle: {
                      color: node.color,
                      shadowColor: 'rgba(0, 0, 0, 0.5)',
                      shadowBlur: 10,
                      zlevel:50,
                      z:50
      
                  },
                  emphasis:{
                    color:"#ffc000",
                    borderCap:'square'
                  },
                  category:node.category
              }:{
                x: node.x,
                y: node.y,
                id: node.id,
                name: node.name,
                symbolSize: node.symbolSize,
                itemStyle: {
                    color: node.color,
                    opacity:0.1
                },
                category:node.category
            };
          }),
            links: linksForGraph.map(function (node) {
              return node.source==toHighlight?{
                  source: node.source,
                  target: node.target,
                  lineStyle:{
                    width:20,

                  },
                  symbolSize:200

              }:{
                source: node.source,
                target: node.target,
                lineStyle:{
                  opacity:0.1,

                }

            };
          }),
            categories: communities,
            roam: true,
            draggable:true,
            selectedMode:'single',
            select:{
                itemStyle:{ 
                color:"#f00",
                borderWidth:2,
                borderColor:'#fff'
            }},
            itemStyle:{
              borderColor:'#fff',
              borderWidth:1,
              borderTYpe:'solid',
              
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
            repulsion: [100,200],
            gravity: 0.2
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
var unHighlight= {
  title: {
      text: 'Les medias',
      subtext: 'Default layout',
      top: 'bottom',
      left: 'right'
  },
  tooltip: {},
  legend: [{
    textStyle: {
      color: "white" ,
      fontWeight:"700",
      fontSize:14
    }            ,
backgroundColor: 'black' ,
/* borderColor:'#fff',
borderWidth:2, */
      //selectedMode: 'single',
      data: communities.map(function (a) {
          return a.name;
      })
  }],
  animationDuration: 1500,
  animationEasingUpdate: 'quinticInOut',
  markPoint:{data:{itemStyle:{
    color: nodesForGraph.map(function (a) {
      return a.color;
  })
  }}

  },
  series: [
      {
          name: 'Media Français',
          type: 'graph',
          layout: 'force',
          data: nodesForGraph.map(function (node) {
            return {
                x: node.x,
                y: node.y,
                id: node.id,
                name: node.name,
                symbolSize: 200,
                itemStyle: {
                    color: node.color,
    
                },
                emphasis:{
                  color:"#ffc000",
                  borderCap:'square'
                },
                category:node.category
            };
        }),
          links: linksForGraph.map(function (node) {
            return {
                source: node.source,
                target: node.target,
 

            };
        }),
          categories: communities,
          roam: true,
          draggable:true,
          selectedMode:'single',
          select:{
              itemStyle:{ 
              color:"#f00",
              borderWidth:2,
              borderColor:'#fff'
          }},
          itemStyle:{
            borderColor:'#fff',
            borderWidth:1,
            borderTYpe:'solid',
            
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
          repulsion: [100,200],
          gravity: 0.2
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

function get_chart(isHighlight,toHighlight)
{
  return isHighlight=='true'?highlight:unHighlight
}

option = {
  title: {
      text: 'Les medias',
      subtext: 'Default layout',
      top: 'bottom',
      left: 'right'
  },
  tooltip: {},
  legend: [{
    textStyle: {
      color: "white" ,
      fontWeight:"700",
      fontSize:14
    }            ,
backgroundColor: 'black' ,
/* borderColor:'#fff',
borderWidth:2, */
      //selectedMode: 'single',
      data: communities.map(function (a) {
          return a.name;
      })
  }],
  animationDuration: 1500,
  animationEasingUpdate: 'quinticInOut',
  markPoint:{data:{itemStyle:{
    color: nodesForGraph.map(function (a) {
      return a.color;
  })
  }}

  },
  series: [
      {
          name: 'Media Français',
          type: 'graph',
          layout: 'force',
          data: nodesForGraph.map(function (node) {
            return node.name=="lemonde.fr"?{
                x: node.x,
                y: node.y,
                id: node.id,
                name: node.name,
                symbolSize: 200,
                itemStyle: {
                    color: node.color,
                    shadowColor: 'rgba(0, 0, 0, 0.5)',
                    shadowBlur: 10,
                    zlevel:50,
                    z:50
    
                },
                emphasis:{
                  color:"#ffc000",
                  borderCap:'square'
                },
                category:node.category
            }:{
              x: node.x,
              y: node.y,
              id: node.id,
              name: node.name,
              symbolSize: node.symbolSize,
              itemStyle: {
                  color: node.color,
                  opacity:0.1
              },
              category:node.category
          };
        }),
          links: linksForGraph.map(function (node) {
            return node.source==indexT?{
                source: node.source,
                target: node.target,
                lineStyle:{
                  width:20,

                },
                symbolSize:200

            }:{
              source: node.source,
              target: node.target,
              lineStyle:{
                opacity:0.1,

              }

          };
        }),
          categories: communities,
          roam: true,
          draggable:true,
          selectedMode:'single',
          select:{
              itemStyle:{ 
              color:"#f00",
              borderWidth:2,
              borderColor:'#fff'
          }},
          itemStyle:{
            borderColor:'#fff',
            borderWidth:1,
            borderTYpe:'solid',
            
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
          repulsion: [100,200],
          gravity: 0.2
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


function get_chart(toHighlight)
  {
    return {
      title: {
          text: 'Les medias',
          subtext: 'Default layout',
          top: 'bottom',
          left: 'right'
      },
      tooltip: {},
      legend: [{
        textStyle: {
          color: "white" ,
          fontWeight:"700",
          fontSize:14
        }            ,
backgroundColor: 'black' ,
/* borderColor:'#fff',
borderWidth:2, */
          //selectedMode: 'single',
          data: communities.map(function (a) {
              return a.name;
          })
      }],
      animationDuration: 1500,
      animationEasingUpdate: 'quinticInOut',
      markPoint:{data:{itemStyle:{
        color: nodesForGraph.map(function (a) {
          return a.color;
      })
      }}

      },
      series: [
          {
              name: 'Media Français',
              type: 'graph',
              layout: 'force',
              data: nodesForGraph.map(function (node) {
                return node.id==toHighlight?{
                    x: node.x,
                    y: node.y,
                    id: node.id,
                    name: node.name,
                    symbolSize: 200,
                    itemStyle: {
                        color: node.color,
                        shadowColor: 'rgba(0, 0, 0, 0.5)',
                        shadowBlur: 10,
                        zlevel:50,
                        z:50
        
                    },
                    emphasis:{
                      color:"#ffc000",
                      borderCap:'square'
                    },
                    category:node.category
                }:{
                  x: node.x,
                  y: node.y,
                  id: node.id,
                  name: node.name,
                  symbolSize: node.symbolSize,
                  itemStyle: {
                      color: node.color,
                      opacity:0.1
                  },
                  category:node.category
              };
            }),
              links: linksForGraph.map(function (node) {
                return node.source==toHighlight?{
                    source: node.source,
                    target: node.target,
                    lineStyle:{
                      width:20,

                    },
                    symbolSize:200

                }:{
                  source: node.source,
                  target: node.target,
                  lineStyle:{
                    opacity:0.1,

                  }

              };
            }),
              categories: communities,
              roam: true,
              draggable:true,
              selectedMode:'single',
              select:{
                  itemStyle:{ 
                  color:"#f00",
                  borderWidth:2,
                  borderColor:'#fff'
              }},
              itemStyle:{
                borderColor:'#fff',
                borderWidth:1,
                borderTYpe:'solid',
                
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
              repulsion: [100,200],
              gravity: 0.2
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
  }