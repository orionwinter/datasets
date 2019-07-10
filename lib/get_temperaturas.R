# devtools::install_github('lhmet/inmetr')
library(inmetr)
library(tidyverse)
library(lubridate)

# descobri a estação que me interessa assim:
# bdmep_meta %>% 
#     filter(name == "Campina Grande")


start_date <- "01/01/2008"
end_date <- format(Sys.Date(), "%d/%m/%Y")

met_data_cg <- bdmep_import(id = 82795,
                            sdate = start_date, 
                            edate = end_date,
                            verbose = TRUE)

# met_data_cj <- bdmep_import(id = 83714,
#                             sdate = start_date, 
#                             edate = end_date, 
#                             verbose = TRUE)

met_data_sp <- bdmep_import(id = 83781,
                            sdate = start_date, 
                            edate = end_date, 
                            verbose = TRUE)

met_data_jp <- bdmep_import(id = 82798,
                            sdate = start_date, 
                            edate = end_date, 
                            verbose = TRUE)

met_data <- bind_rows(
  "Campina Grande" = met_data_cg, 
  # "Campos do Jordão" = met_data_cj, 
  "São Paulo" = met_data_sp, 
  "João Pessoa" = met_data_jp,
  .id = "cidade"
  )

por_dia <- met_data %>% 
  mutate(dia = floor_date(date, unit = "day")) %>% 
  group_by(cidade, dia) %>% 
  summarise(tmedia = mean(tair), 
            tmax = max(tmax, na.rm = T), 
            tmin = max(tmin, na.rm = T), 
            chuva = sum(prec, na.rm = T)) %>% 
  filter(!is.na(tmedia), !is.infinite(tmax), !is.infinite(tmin))  

# por_dia %>% 
#   write_csv("../docs/clima-diario.csv")

por_semana <- por_dia %>% 
  mutate(semana = lubridate::floor_date(dia, unit = "weeks"),
         ano = year(semana),
         mes = month(semana)) %>% 
  group_by(cidade, semana, mes, ano) %>% 
  summarise(tmedia = mean(tmedia), 
            tmax = max(tmax), 
            tmin = min(tmin), 
            chuva = sum(chuva))

por_semana %>% 
  filter(ano >= year(dmy(start_date))) %>% 
  write_csv("../docs/clima_cg_jp_sp-semanal-2.csv")
