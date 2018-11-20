library(readr)
library(tidyverse)
rnj <- read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/running time/rnj.csv") %>% mutate(algorithm = 'rapidnj')
qt <- read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/running time/quicktree.csv") %>% mutate(algorithm = 'quicktree')
langhave <- read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/running time/langhave.csv") %>% mutate(algorithm = 'langhave')

data = bind_rows(rnj, qt) %>% bind_rows(langhave)

data %>% ggplot(aes(x = taxa, y = time, color = algorithm)) +
    geom_point() + 
    geom_line() +
    scale_y_sqrt() + 
    labs(title = "Running time of algorithms",
         subtitle = "The y-axis is visually square root scaled.",
         x = "taxa",
         y = "time [seconds]")


data %>% select(-file) %>%  spread(algorithm, time) %>%
    mutate(quicktree / langhave) %>%
    mutate(rapidnj / langhave) %>%
    
    arrange(taxa) %>% View

