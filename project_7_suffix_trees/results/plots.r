#library(readr)
library(tidyverse)
library(gridExtra)
data <- read_csv("Biologi/AiB/gr_AiB_naotei/project_7_suffix_trees/results/out.csv")

data_mod = data[-1,] %>% mutate(size = (size)/3, search_time = search_time)


p1 = data_mod %>% ggplot(aes(size, constr_time)) + 
    geom_point(alpha = 0.7) + 
    labs(title = "Construction of suffix tree", x = "", y = "construction time [s]")

p2 = data_mod %>% ggplot(aes(size, constr_time/(log(size)*size^2))) + 
    geom_point(alpha = 0.7) + 
    labs(x = "genome size = n", y = "constr_time / (log(n) * n^2)")
    
p3 = data_mod %>% ggplot(aes(size, constr_time/(size^2))) + 
    geom_point(alpha = 0.7) +
    labs(x = "genome size = n", y = "constr_time / n^2")
    
    

grid.arrange(p1, p2, p3, ncol = 1)



q1 = data_mod %>% ggplot(aes(size, search_time)) + 
    geom_point(alpha = 0.7) + 
    labs(title = "Search time", x = "", y = "search_time [s]")

q2 = data_mod %>% ggplot(aes(size, search_time/size)) + 
    geom_point(alpha = 0.7) + 
    labs(title = "", x = "genome size = n", y = "search_time / n")



grid.arrange(q1, q2, ncol = 1)




