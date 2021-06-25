
        function search() {
            var query=$("#search").find("input[name=search]").val();
            $.get("/search?q=" + encodeURIComponent(query),
                    function (data) {
                        var t = $("table#results tbody").empty();
                        if (!data || data.length == 0) return;
                        data.forEach(function (media) {
                            $("<tr><td class='media'>" + media.site_name + "</td><td>" + media.type + "</td><td>" + media.entity + "</td><td>").appendTo(t)
                                    .click(function() { showDetails($(this).find("td").text()); get_info($(this).find("td.media").text());})
                                    .click(function() { console.log($(this).find("td").text());})
                                    //.click(function() { console.log("fonction1 ici", $(this).find("td.media").text());})
                                        //.submit(testfunc)
                                    //.click(function() { testfunc();})
                        });
                        showDetails(data[0].site_name);
                    }, "json");
            //console.log("search", query)
            return false;
        }

function entityButtonFunction() {
    var graph_type = "/ent_graph";
    console.log(graph_type);
}
function websiteButtonFunction() {
    var graph_type = "/web_graph";
    console.log(graph_type);
}
function twitterButtonFunction() {
    var graph_type = "/twit_graph";
    console.log(graph_type);
}
function youtubeButtonFunction() {
    var graph_type = "/yout_graph";
    console.log(graph_type);
}

function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

// Color function
function circleColour(d){
	return catColScale(d.Community);
	//return d.color;
}

function linkColour(d){
    return contColLinkScale(d.count)
	//return d.color;
}

function linkThick(d){
    return contLinkScale(d.count)
}
function highlightNodeSearch(name_search){
            var theNode = d3.selectAll('circle')
                  //.data(nodes, function (node) { return node.id })
                  .filter(function(d) { return d.name == name_search });
            var theText = d3.selectAll('text')
                .filter(function(d) { return d.name == name_search });


            //console.log("name_search", name_search);
            d3.selectAll('circle').style("opacity","0.3")
            d3.selectAll('text').style("opacity","0.3")
            d3.selectAll('line').style("stroke-opacity","0.3")

            theNode.style("opacity","1").style("stroke-width","10px");
            theText.style("opacity","1");
        }


function showDetails(site_name) {
    $.get("/media/" + encodeURIComponent(site_name),
            function (data) {
              console.log("data",data)
                var t = $("table#dlinks tbody").empty();
                //var e = $("table#entity tbody").empty();
                highlightNodeSearch(data[0].d_sitename);
                //console.log("fonc3", data[0].d_sitename);
                if (!data || data.length == 0) return;
                $("#title_entity").text(data[0].entity_name);
                $("#title_details").text(data[0].d_title);
                $("#dname").text(data[0].d_name );
                $("#dloc").text(data[0].d_loc );
                $("#dstats1").text(data[0].d_stat1);
                $("#dstats2").text(data[0].d_stat2);
                $("#dDAT").text(data[0].d_DAT);
                $("#eMondiplo").text(data[0].e_diplo );
                $("#ewikisummary").text(data[0].e_wikisummary );
                $("#eSpiil").text(data[0].e_Spiil );
                $("#eCPPAP").text(data[0].e_CPPAP );
                $("#eML").text(data[0].e_ML );
                data.forEach(function (media) {
                    $("<tr><td class='media'>" + media.site_name+ "</td><td>" + media.type + "</td><td>" + media.cite + "</td><td>" + media.estcite + "</td><td>").appendTo(t)
                            //.click(function() { console.log("fonction2 ici:",$(this).find("td.media").text());})
                            .click(function() {highlightNodeSearch($(this).find("td.media").text());})
                    //$("<tr><td class='media'>" + media.entity_type+ "</td><td>").appendTo(e)
                });
            }, "json");
    //console.log("media", site_name)
    return false;
}

function nodeSize(d){
    return nodeSizeScale(d.size)
}

function getNeighbors(node) {
  return baseLinks.reduce(function (neighbors, link) {
      if (link.target.id === node.id) {
        neighbors.push(link.source.id)
      } else if (link.source.id === node.id) {
        neighbors.push(link.target.id)
      }
      return neighbors
    },
    [node.id]
  )
}


function isNeighborLink(node, link) {
  return link.target.id === node.id || link.source.id === node.id
}

function isNeighborNode(node, link) {
  return (Array.isArray(link) && link.indexOf(node.id) > -1)
}

function getNodeColor(node, neighbors) {
  if (Array.isArray(neighbors) && neighbors.indexOf(node.id) > -1) {
    return node.level === 1 ? 'blue' : 'green'
  }

  return node.level === 1 ? 'red' : 'gray'
}


function getLinkColor(node, link) {
  return isNeighborLink(node, link) ? 'green' : '#E5E5E5'
}

function getTextColor(node, neighbors) {
  return Array.isArray(neighbors) && neighbors.indexOf(node.id) > -1 ? 'green' : 'black'
}

// updates the colors of all nodes, texts and links depending on "neighboring status"
function highlightNode(selectedNode) {
    const neighbors = getNeighbors(selectedNode)
    nodeElements
      .style('stroke-width', node => isNeighborNode(node, neighbors) ? 6 : 2)
      //.attr('fill', node => isNeighborNode(node, neighbors) ? 'blue' : circleColour(node))
      .style('opacity', node => isNeighborNode(node, neighbors) ? 1 : 0.3)
    textElements
      .attr('fill', node => isNeighborNode(node, neighbors) ? "white" : "white")
      .style("font-weight", node => isNeighborNode(node, neighbors) ? "bold" : "normal")
      .style('opacity', node => isNeighborNode(node, neighbors) ? 1 : 0.3)
    linkElements
      .style('stroke-width', link => isNeighborLink(selectedNode, link) ? 3 : 1)
      .style('stroke-opacity', link => isNeighborLink(selectedNode, link) ? 0.8 : 0.3)
      //.style('stroke', link => isNeighborLink(selectedNode, link) ? "blue" : "gray")
  }
  

function unHighlightNode(selectedNode) {
    const neighbors = getNeighbors(selectedNode)
    nodeElements
      .style('stroke-width', 2)
      //.attr('fill', node => isNeighborNode(node, neighbors) ? 'blue' : circleColour(node))
      .style('opacity', node => isNeighborNode(node, neighbors) ? 1 : 1)
    textElements
      .attr('fill', node => isNeighborNode(node, neighbors) ? "white" : "white")
      .style("font-weight", node => isNeighborNode(node, neighbors) ? "bold" : "normal")
      .style('opacity', 1)
    linkElements
      .style('stroke-width', 1)
      .style('stroke-opacity', 0.8)
      //.style('stroke', link => isNeighborLink(selectedNode, link) ? "blue" : "gray")
  
  }

// select node is called on every click
// we either update the data according to the selection
// or reset the data if the same node is clicked twice
function selectNode(selectedNode) {
    if (selectedId === selectedNode.id) {
      selectedId = undefined
      highlightNode(selectedNode)
      resetData()
      console.log(selectedNode)
      showDetails(selectedNode.name+'Website')
      
      //updateSimulation()
      
    } else {
      selectedId = selectedNode.id
      highlightNode(selectedNode)
      updateData(selectedNode)
      //updateSimulation()
      showDetails(selectedNode.name+'Website')
      
      //highlightNode(selectedNode)
      console.log("Else",selectedNode.name+'Website')
    }
  
    var neighbors = getNeighbors(selectedNode)
  
    // we modify the styles to highlight selected nodes
    //nodeElements.attr('fill', function (node) { return getNodeColor(node, neighbors) })
    //textElements.attr('fill', function (node) { return getTextColor(node, neighbors) })
    //linkElements.attr('stroke', function (link) { return getLinkColor(selectedNode, link) })
  }
  
  
  

// this helper simple adds all nodes and links
// that are missing, to recreate the initial state
function resetData() {
    var nodeIds = nodes.map(function (node) { return node.id })
  
    baseNodes.forEach(function (node) {
      if (nodeIds.indexOf(node.id) === -1) {
        nodes.push(node)
      }
    })
  
    links = baseLinks
  }

// diffing and mutating the data
function updateData(selectedNode) {
    var neighbors = getNeighbors(selectedNode)
    var newNodes = baseNodes.filter(function (node) {
      return neighbors.indexOf(node.id) > -1 || node.level === 1
    })
  
    var diff = {
      removed: nodes.filter(function (node) { return newNodes.indexOf(node) === -1 }),
      added: newNodes.filter(function (node) { return nodes.indexOf(node) === -1 })
    }
  
    diff.removed.forEach(function (node) { nodes.splice(nodes.indexOf(node), 1) })
    diff.added.forEach(function (node) { nodes.push(node) })
  
    links = baseLinks.filter(function (link) {
      return link.target.id === selectedNode.id || link.source.id === selectedNode.id
    })
  }

function updateGraph() {
    // links
    linkElements = linkGroup.selectAll('line')
      .data(links, function (link) {
        return link.target.id + link.source.id
      })
  
    linkElements.exit().remove()
  
    var linkEnter = linkElements
      .enter().append('line')
      .attr("class", "links")
      .style('stroke-width', linkThick)
      .attr('stroke', linkColour)
  
    linkElements = linkEnter.merge(linkElements)
  
    // nodes
    nodeElements = nodeGroup.selectAll('circle')
      .data(nodes, function (node) { return node.id })
  
    nodeElements.exit().remove()
  
    var nodeEnter = nodeElements
      .enter()
      .append('circle')
      .attr("class", "nodes")
      .attr("r", nodeSize)
      //.attr("r", function (d) { return d.size * 10; })
      .attr('fill', circleColour)
      .call(dragDrop)
      .on('mouseover', highlightNode)
      .on("mouseout", unHighlightNode)
      // we link the selectNode method here
      // to update the graph on every click
      .on('click', selectNode)
  
    nodeElements = nodeEnter.merge(nodeElements)
  
    // texts
    textElements = textGroup.selectAll('text')
      .data(nodes, function (node) { return node.id })
  
    textElements.exit().remove()
  
    var textEnter = textElements
      .enter()
      .append('text')
      .text(function (node) { return node.name })
      .attr("class", "texts")
      .style("font-size", nodeSize)
      //.style("font-size", function (node) { return node.size *10 +10 })
      .attr('fill', "white")
      .style('opacity', 1)
      .attr('dx', 15)
      .attr('dy', 4)
  
    textElements = textEnter.merge(textElements)
  }
  
  function updateSimulation() {
    updateGraph()
  
    simulation.nodes(nodes).on('tick', () => {
      nodeElements
        .attr('cx', function (node) { return node.x })
        .attr('cy', function (node) { return node.y })
      textElements
        .attr('x', function (node) { return node.x })
        .attr('y', function (node) { return node.y })
      linkElements
        .attr('x1', function (link) { return link.source.x })
        .attr('y1', function (link) { return link.source.y })
        .attr('x2', function (link) { return link.target.x })
        .attr('y2', function (link) { return link.target.y })
    })
  
    simulation.force('link').links(links)
    simulation.alphaTarget(0.7).restart()
  }