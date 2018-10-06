library(tidyverse)

approx = read_csv("Biologi/AiB/gr_AiB/project_3_multiple/running_time/sp_approx.csv", col_names = T) %>% mutate(alg = "2-approx") 
exact = read_csv("Biologi/AiB/gr_AiB/project_3_multiple/running_time/sp_exact_3.csv", col_names = T) %>% mutate(alg = "exact 3") 

data = bind_rows(approx, exact)




ggplot(data) +
    geom_line(aes(len, t,  color = alg)) +
    geom_point(aes(len,  t, color = alg)) +
    labs(x = "sequence length (letters)", y = "time (seconds)", title = "Running time") + 
    scale_color_discrete(guide = guide_legend(title = "algorithm"))


ggplot(filter(data, alg == "2-approx")) +
    geom_line(aes(len, t^(1/2)/len))

ggplot(filter(data, alg == "exact 3")) +
    geom_line(aes(len, t^(1/3)/len))


ratios = approx$score/exact$score
ratio_data = tibble(len = 1:length(ratios), r = ratios)
ggplot(ratio_data) + 
    geom_line(aes(len, r)) +
    geom_point(aes(len, r)) +
    labs(x = "sequence length (letters)", y = "ratio (approx/exact)", title = "Ratio between the score of two algorithms")


