library(shiny)
library(dplyr)
player <- 'LeBron James'

data <- read.csv('./base_data_23-24.csv')

x <- data[,-1] |> colnames()

for (col in x) {
  data[,col] <- data[,col] |> percent_rank()
} 

ui <- fluidPage(
  titlePanel("Percentile Plot"),
  sidebarLayout(
    sidebarPanel(
      selectInput('player', "Player:", 
                  choices=unique(data$PLAYER_NAME))
    ),
    mainPanel(
      plotOutput('plot')
    )
  )
)

server <- function(input, output) {

  y <- reactive({data[data$PLAYER_NAME == input$player,-1] |> as.numeric()})
  output$plot <- renderPlot({
    barplot(y() ~ x, ylim=c(0,1))
  })
}


shinyApp(ui = ui, server = server)
