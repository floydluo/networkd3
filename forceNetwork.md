Create a D3 JavaScript force directed network graph.

# Description

Create a D3 JavaScript force directed network graph.

#Usage

```
forceNetwork(Links,
             Nodes,
             Source,
             Target,
             Value,
             NodeID,
             Nodesize,
             Group,
             height = NULL,
             width = NULL,
             colourScale = JS("d3.scale.category20()"),
             fontSize = 7,
             fontFamily = "serif",
             linkDistance = 50,
             linkWidth = JS("function(d) { return Math.sqrt(d.value); }"),

             radiusCalculation = JS(" Math.sqrt(d.nodesize)+6"),
             charge = -120,
             linkColour = "#666",
             opacity = 0.6,
             zoom = FALSE,
             legend = FALSE,
             bounded = FALSE,
             opacityNoHover = 0,
             clickAction = NULL)
```

Arguments

1. Links

a `data frame` object with the links between the nodes. It should include the `Source` and `Target` for each link. `These should be numbered starting from 0.` An optional `Value` variable can be included to specify how close the nodes are to one another.

2. Nodes

a `data frame` containing the `node id` and `properties` of the nodes. If no ID is specified then the nodes must be in the same order as the `Source` variable column in the Links data frame. Currently only a grouping variable is allowed.

3. Source

character string naming the network source variable in the `Links data frame`.

4. Target

character string naming the network target variable in the `Links data frame`.

5. Value

character string naming the variable in the `Links data frame` for how wide the links are.

6. NodeID

character string specifying the node IDs in the `Nodes data frame`.

7. Nodesize

character string specifying the a column in the Nodes data frame with some value to vary the node radius's with. See also radiusCalculation.

8. Group

character string specifying the group of each node in the `Nodes data frame`.

9. height

numeric height for the network graph's frame area in pixels.

10. width

numeric width for the network graph's frame area in pixels.

11. **colourScale**

character string specifying the categorical colour scale for the nodes. See https://github.com/mbostock/d3/wiki/Ordinal-Scales.

12. fontSize

numeric font size in pixels for the node text labels.

13. fontFamily

font family for the node text labels.

14. linkDistance

numeric or character string. Either numberic fixed distance between the links in pixels (actually arbitrary relative to the diagram's size). Or a JavaScript function, possibly to weight by Value. For example: `linkDistance = JS("function(d){return d.value * 10}")`.

15. linkWidth

numeric or character string. Can be a numeric fixed width in pixels (arbitrary relative to the diagram's size). Or a JavaScript function, possibly to weight by Value. The default is `linkWidth = JS("function(d) { return Math.sqrt(d.value); }")`.

16. radiusCalculation

character string. A javascript mathematical expression, to weight the radius by Nodesize. The default value is `radiusCalculation = JS("Math.sqrt(d.nodesize)+6")`.

17. charge	(to attract or to avoid)

numeric value indicating either the strength of the node repulsion (negative value) or attraction (positive value).

18. **linkColour**

character vector specifying the colour(s) you want the link lines to be. Multiple formats supported (e.g. hexadecimal).

19. opacity

numeric value of the proportion opaque you would like the graph elements to be.

20. zoom

logical value to enable (TRUE) or disable (FALSE) zooming.

21. legend

logical value to enable node colour legends.

22. bounded

logical value to enable (TRUE) or disable (FALSE) the bounding box limiting the graph's extent. See http://bl.ocks.org/mbostock/1129492.

23. opacityNoHover

numeric value of the opacity proportion for node labels text when the mouse is not hovering over them.

24. clickAction

character string with a JavaScript expression to evaluate when a node is clicked.


Source

D3.js was created by Michael Bostock. See http://d3js.org/ and, more specifically for force directed networks https://github.com/mbostock/d3/wiki/Force-Layout.

See Also

JS.

Examples

# Load data
data(MisLinks)
data(MisNodes)
# Create graph
forceNetwork(Links = MisLinks, Nodes = MisNodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 0.4, zoom = TRUE)

# Create graph with legend and varying node radius
forceNetwork(Links = MisLinks, Nodes = MisNodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Nodesize = "size",
             radiusCalculation = "Math.sqrt(d.nodesize)+6",
             Group = "group", opacity = 0.4, legend = TRUE)

## Not run:
#### JSON Data Example
# Load data JSON formated data into two R data frames
# Create URL. paste0 used purely to keep within line width.
URL <- paste0("https://cdn.rawgit.com/christophergandrud/networkD3/",
              "master/JSONdata/miserables.json")

MisJson <- jsonlite::fromJSON(URL)

# Create graph
forceNetwork(Links = MisJson$links, Nodes = MisJson$nodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 0.4)

# Create graph with zooming
forceNetwork(Links = MisJson$links, Nodes = MisJson$nodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 0.4, zoom = TRUE)


# Create a bounded graph
forceNetwork(Links = MisJson$links, Nodes = MisJson$nodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 0.4, bounded = TRUE)

# Create graph with node text faintly visible when no hovering
forceNetwork(Links = MisJson$links, Nodes = MisJson$nodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 0.4, bounded = TRUE,
             opacityNoHover = TRUE)

## Specify colours for specific edges
# Find links to Valjean (11)
which(MisNodes == "Valjean", arr = TRUE)[1] - 1
ValjeanInds = which(MisLinks == 11, arr = TRUE)[, 1]

# Create a colour vector
ValjeanCols = ifelse(1:nrow(MisLinks) %in% ValjeanInds, "#bf3eff", "#666")

forceNetwork(Links = MisLinks, Nodes = MisNodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 0.8, linkColour = ValjeanCols)


## Create graph with alert pop-up when a node is clicked.  You're
# unlikely to want to do exactly this, but you might use
# Shiny.onInputChange() to allocate d.XXX to an element of input
# for use in a Shiny app.

MyClickScript <- 'alert("You clicked " + d.name + " which is in row " +
       (d.index + 1) +  " of your original R data frame");'

forceNetwork(Links = MisLinks, Nodes = MisNodes, Source = "source",
             Target = "target", Value = "value", NodeID = "name",
             Group = "group", opacity = 1, zoom = FALSE,
             bounded = TRUE, clickAction = MyClickScript)

## End(Not run)
