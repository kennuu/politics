library(dplyr)
library(ggplot2)

data <- read.csv('hs2019ek/data/partymatches.csv', sep = ';')
ekpuolue <- c('Keskusta', 'Kokoomus', 'Kristillisdemokraatit', 'Liike Nyt', 'Perussuomalaiset', 'Ruotsalainen kansanpuolue', 
              'SDP', 'Sininen tulevaisuus', 'Vasemmistoliitto', 'Vihreat')

data <- data %>%
  mutate(ekpuolue = puolue %in% ekpuolue)



ggplot(data, aes(x = as.numeric(row.names(data)), y = oma_puolue, color = ekpuolue)) + geom_point()

data <- data %>%
  filter(puolue == 'Vihreat')
  select(Vihreat, Feministinen.puolue)
ggplot(data, aes(x = as.numeric(row.names(data)), y = Feministinen.puolue)) + geom_point()
ggplot(data, aes(x = as.numeric(row.names(data)), y = oma_puolue)) + geom_point()

       