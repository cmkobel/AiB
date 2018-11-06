library(readr)
library(tidyverse)
library(latex2exp)
t2 <- read_csv("C:/Users/Trash/Biologi/AiB/gr_AiB_trashmaster/project_4_tree/experiment5/t1.csv")


t2 %>% ggplot(aes(iplusone, time)) + 
  geom_line() + 
  geom_smooth(method = "lm", formula = "y ~ I(x^2)", size = 0.5, se = F) + 
  labs(title = "Running time of RF-distance between two trees",
       subtitle = TeX("blue line: linear regression: $y ~ x^2$"),
       x = "tree size (taxa)",
       y = "time (seconds)")

t2 %>% ggplot(aes(iplusone, time^(1/2)/iplusone)) + 
  geom_line() + 
  labs(title = "Running time of RF-distance between two trees",
       x = "tree size (taxa)",
       y =TeX("normalized time: $\\frac{\\sqrt{time}}{|taxa|}$"))



