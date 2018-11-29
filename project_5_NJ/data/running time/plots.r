library(readr)
library(tidyverse)
rnj <- read_csv("rnj.csv") %>% mutate(algorithm = 'Rapid NJ')
qt <- read_csv("quicktree.csv") %>% mutate(algorithm = 'QuickTree')
langhave <- read_csv("langhave.csv") %>% mutate(algorithm = 'generic NJ')

data = bind_rows(rnj, qt) %>% bind_rows(langhave)

data %>% ggplot(aes(x = taxa, y = time, color = algorithm)) +
    geom_point() + 
    geom_line() +
    scale_y_sqrt() + 
    labs(title = "Running time of algorithms",
         subtitle = "The y-axis is visually square root scaled.",
         x = "taxa",
         y = "time [seconds]")


# RF distances
rq_rfdist = read_csv("../rfdist/rnjmodqt/rq_rfdist.csv") %>% select(-file)

our_rfdist = read_csv("../rfdist/voresmodandre/ours.csv") %>% select(-file) %>% spread(comparison, rfdist)

data %>% select(-file) %>%  spread(algorithm, time) %>%
    mutate(QuickTree / `generic NJ`) %>%
    mutate(`Rapid NJ` / `generic NJ`) %>%
    left_join(rq_rfdist) %>%
    #select(-taxa1) %>% 
    left_join(our_rfdist[1:3]) %>% View
    knitr::kable("html", 2)
