library(ggplot2)
library(dplyr)
library(ggrepel)
library(stringr)
library(data.table)

candidates <- read.csv('../data/yle_2019_mep_factors.csv')
governments <- read.csv('../data/yle_2019_governments.csv') %>%
  # filter(!str_detect(parties, 'KESK')) %>%
  setDT(keep.rownames = TRUE) %>%
  mutate(label = paste0(rn, ': ', parties, ' ', format(round(std_norm, 2), nsmall = 2), ' ', format(round(disttoSDP, 2), nsmall = 2), 
                        ' ', format(round(std_c_norm, 2), nsmall = 2)))

party_means = candidates %>%
  group_by(puolue) %>%
  summarise(PA1_mean = mean(PA1),
            PA2_mean = mean(PA2))

head(governments)
ggplot(data=candidates, aes(x = PA1, y = PA2)) + geom_point(data=candidates, aes(color = puolue)) + 
  geom_point(data=party_means, aes(x=PA1_mean, y=PA2_mean, color=puolue), shape=17, size=5) + 
  geom_text_repel(data=party_means, aes(x=PA1_mean, y=PA2_mean, label=puolue)) +
  geom_point(data=head(governments, 10), aes(x = PA1_mean, y = PA2_mean), shape=16, size=3) +
  geom_text_repel(data=head(governments, 10), aes(x = PA1_mean, y = PA2_mean, label = label), size=5) 

governments <-governments %>%
  arrange(std_c_norm) %>%
  select(-rn) %>%
  setDT(keep.rownames = TRUE) %>%
  mutate(label_c = paste0(rn, ': ', parties))

ggplot(data=candidates, aes(x = PA1, y = PA2)) + geom_point(data=candidates, aes(color = puolue)) + 
  geom_point(data=party_means, aes(x=PA1_mean, y=PA2_mean, color=puolue), shape=17, size=5) + 
  geom_text_repel(data=party_means, aes(x=PA1_mean, y=PA2_mean, label=puolue)) +
  geom_point(data=head(governments, 10), aes(x = PA1_c_mean, y = PA2_c_mean), shape=16, size=3) +
  geom_text_repel(data=head(governments, 10), aes(x = PA1_c_mean, y = PA2_c_mean, label = label_c), size=5) 
