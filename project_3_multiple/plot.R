library(tidyverse)

approx = read_csv("Biologi/AiB/gr_AiB/project_3_multiple/running_time/sp_approx.csv", col_names = T) %>% mutate(alg = "2-approx") 
exact = read_csv("Biologi/AiB/gr_AiB/project_3_multiple/running_time/sp_exact_3.csv", col_names = T) %>% mutate(alg = "exact 3") 

data = bind_rows(approx, exact)

# overview
ggplot(data) +
    geom_line(aes(len, t,  color = alg)) +
    geom_point(aes(len,  t, color = alg)) +
    labs(x = "sequence length (letters)", y = "time (seconds)", title = "Running time of two algorithms") + 
    scale_color_discrete(guide = guide_legend(title = "algorithm"))

# 2-approx normalized
ggplot(filter(data, alg == "2-approx"), aes(len, t^(1/2)/len)) +
    geom_line() +
    geom_point() +
    labs(x = "sequence length (letters)", y = "normalized time (t^(1/2) / |input|)", title = "Running time of 2-approx.")

# exact 3 normalized
ggplot(filter(data, alg == "exact 3"), aes(len, t^(1/3)/len)) +
    geom_line() +
    geom_point() +
    labs(x = "sequence length (letters)", y = "normalized time (t^(1/3) / |input|)", title = "Running time of exact 3")

# ratio
max_ratio = tibble(
    len = seq(10, 200),
    r = 2-2/len,
    algorithm = "theoretical max (2-2/m)"
)

ratios = approx$score/exact$score
ratio_data = tibble(len = 1:length(ratios)*10, r = ratios, algorithm = "measured") %>%
    bind_rows(max_ratio)


ggplot(ratio_data, aes(len, r, color = algorithm)) + 
    geom_line() +
    geom_point(data = filter(ratio_data, algorithm == "measured")) +
    labs(x = "sequence length: m (letters)", y = "ratio (2_approx. / exact_3)", title = "Ratio between the score of two algorithms") +
    theme(legend.position="bottom")


