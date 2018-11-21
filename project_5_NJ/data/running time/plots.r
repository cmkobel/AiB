library(readr)
library(tidyverse)
rnj <- read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/running time/rnj.csv") %>% mutate(algorithm = 'Rapid NJ')
qt <- read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/running time/quicktree.csv") %>% mutate(algorithm = 'QuickTree')
langhave <- read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/running time/langhave.csv") %>% mutate(algorithm = 'generic NJ')

data = bind_rows(rnj, qt) %>% bind_rows(langhave)

data %>% ggplot(aes(x = taxa, y = time, color = algorithm)) +
    geom_point() + 
    geom_line() +
    scale_y_sqrt() + 
    labs(title = "Running time of algorithms",
         subtitle = "The y-axis is visually square root scaled.",
         x = "taxa",
         y = "time [seconds]")

rq_rfdist = read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/rfdist/rnjmodqt/rq_rfdist.csv") %>% select(-file)

our_rfdist = read_csv("Biologi/AiB/gr_AiB_naotei/project_5_NJ/data/rfdist/voresmodandre/our_rfdist.csv") %>% select(-file)

data %>% select(-file) %>%  spread(algorithm, time) %>%
    mutate(QuickTree / `generic NJ`) %>%
    mutate(`Rapid NJ` / `generic NJ`) %>%
    bind_cols(rq_rfdist) %>%
    select(-taxa1) %>% View

