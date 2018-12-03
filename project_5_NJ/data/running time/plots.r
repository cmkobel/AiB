library(readr)
library(tidyverse)
rnj <- read_csv("rnj.csv") %>% mutate(algorithm = 'Rapid NJ')
qt <- read_csv("quicktree.csv") %>% mutate(algorithm = 'QuickTree')
#langhave <- read_csv("langhave.csv") %>% mutate(algorithm = 'generic NJ')
kobel = read_csv("../../parallel_output/times_copy.csv")

data = bind_rows(rnj, qt) %>% bind_rows(kobel)

data %>% ggplot(aes(x = taxa, y = time, color = algorithm)) +
    geom_point() + 
    geom_line() +
    scale_y_log10() + 
    labs(title = "Running time of algorithms",
         subtitle = "The y-axis is visually log_10 scaled.",
         x = "|taxa|",
         y = "time [seconds]")

data %>% filter(algorithm == "Our Saitou Nei") %>% 
    ggplot(aes(x = taxa, y = time^(1/3)/taxa)) + 
    geom_line() + 
    geom_point() + 
    labs(y = "normalized time: time^(1/3) / |taxa|",
         x = "|taxa|",
         title = "Running time of our implementation",
         subtitle = "Saitou Nei's Neighbour Joining") 


# RF distances
rq_rfdist = read_csv("../rfdist/rnjmodqt/rq_rfdist.csv") %>% select(-file)

#langhave_rfdist = read_csv("../rfdist/voresmodandre/ours.csv") %>% select(-file) %>% spread(comparison, rfdist)

kobel_qt_rfdist = read_csv("../rfdist/kobelmodandre/ourVSqt.csv") %>% select(-file)
kobel_rnj_rfdist = read_csv("../rfdist/kobelmodandre/ourVSrnj.csv") %>% select(-file)


df = data %>% select(-file) %>%  spread(algorithm, time) %>%
    mutate(QuickTree / `Our Saitou Nei`) %>%
    mutate(`Rapid NJ` / `Our Saitou Nei`) %>%
    left_join(rq_rfdist) %>%
    #select(-taxa1) %>% 
    #left_join(our_rfdist[1:3]) %>% View
    left_join(kobel_qt_rfdist) %>% 
    left_join(kobel_rnj_rfdist)

df %>% knitr::kable("html")

df[c(1,7,8,9)] %>% gather(algorithm, rfdist, -taxa) %>%
    ggplot((aes(taxa, rfdist, color = algorithm))) +
    geom_point() +
    geom_line() + 
    labs(title = "RF-distances of trees from different algorithms",
         y = "RF-distance")


