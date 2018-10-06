library(tidyverse)

approx = read_csv("Biologi/AiB/gr_AiB/project_3_multiple/running_time/sp_approx.csv", col_names = T) %>% mutate(alg = "2-approx") 
exact = read_csv("Biologi/AiB/gr_AiB/project_3_multiple/running_time/sp_exact_3.csv", col_names = T) %>% mutate(alg = "exact 3") 

data = bind_rows(approx, exact)




ggplot(data) +
    geom_line(aes(len, t,  color = alg)) +
    geom_point(aes(len,  t, color = alg)) +
    labs(x = "sequence length (letters)", y = "time (seconds)", title = "running time") + 
    scale_color_discrete(guide = guide_legend(title = "algorithm")) +
    scale_y_sqrt()

