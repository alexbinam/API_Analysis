## START SCRIPT HERE
library(dplyr)
library(httr)
library(jsonlite)
library(ggplot2)
library(plyr)

# Google Civics
google.key <- 'AIzaSyBT0G6HCQ-JYwD8z7AiO7jyWUmTuSEla8o'
address <- '329 Hillwick Ln., Schaumburg, IL 60193'
google.url <- "https://www.googleapis.com/civicinfo/v2/representatives"

# Propublica
propublica.key <- 'gI6KctGaork7Bfhn5zh0uAKBInxgY9VhN8g1bGFc'
names(propublica.key) <- "X-API-Key"
senate.url <- 'https://api.propublica.org/congress/v1/115/senate/members.json'




GetCivicData <- function(anAddress, aKey){
  query_parameters <- list(address=anAddress,
                           key=aKey)
  
  civic_data <- GET(google.url, query = query_parameters) %>% 
    content('text') %>% 
    fromJSON()
  
  return(civic_data)
}


CreateSenatorsDf <- function(url, key){
  senate_results <- GET(url, add_headers(.headers = key), 
                        content_type_json()) %>% content('parsed')
  
  senate_members <- ldply(senate_results$results[[1]]$members, 
                          .fun=function(x){
                            as.data.frame(x[!sapply(x, is.null)])
                          }
  )
  
  return(senate_members)
}


our_civic_results <- GetCivicData(address, google.key)
our_civic_results$officials


senate_df <- CreateSenatorsDf(senate.url, propublica.key)


# Write a function that takes in address, parses state, and returns contact links for senators from that state
address <- '329 Hillwick Ln., Schaumburg, IL 60193'

library(stringr)

WriteYourSenators <- function(address){
  
  # Grab state
  comma.locs <- str_locate_all(address, ',')
  second.comma.i <- comma.locs[[1]][2]
  state <- str_trim(substring(address, second.comma.i+1, second.comma.i+3))
  
  # Get links of senators from that state
  senator.locs <- which(senate_df$state == state)
  listOfLinks <- list(senate_df[senator.locs, 'contact_form'])
  
  return(listOfLinks)
}

WriteYourSenators('1510 NW 124th Ave, Portland, OR 97229')

str(senate_df)
senate_df$in_office
senate_df[senate_df$in_office == FALSE,]

senate_df <- senate_df[senate_df$in_office== TRUE,]
senate_df <- senate_df[senate_df$in_office,]
dim(senate_df)

str(senate_df)
senate_df$total_votes



## To start, let's pull the quantiative variables of interest
quant_cols <- c('dw_nominate', 'missed_votes', 'total_present', 'missed_votes_pct', 'votes_with_party_pct', 'seniority')
quant_col_i <- colnames(senate_df) %in% quant_cols

senate_df_quant <- senate_df[,quant_col_i]
senate_df_quant$seniority <- as.numeric(senate_df_quant$seniority)


gen_sen_missed_votes_plot <- function(member_df){
  p <- ggplot(member_df, aes(x=as.numeric(seniority), y=missed_votes_pct)) +
    geom_point(size=1, shape=1) + 
    labs(title = 'Relationship Between Representative Seniority and Missed Votes Percentage',
         x = 'Seniority',
         y = 'Missed Votes Percentage')
  return(p)
}

gen_sen_missed_votes_plot(senate_df_quant)


gen_sen_hist <- function(sen_df){
  p <- ggplot(data = sen_df, aes(party)) + 
    geom_bar() + 
    labs(title = 'Count of 2017 Senate Members by Party', 
         y = 'Frequency', 
         x = 'Party') + 
    coord_flip()
  return(p)
}

gen_sen_hist(senate_df)


### Call API with Senator uri's
GetYourSenatorsAPI <- function(address){
  
  # Grab state
  comma.locs <- str_locate_all(address, ',')
  second.comma.i <- comma.locs[[1]][2]
  state <- str_trim(substring(address, second.comma.i+1, second.comma.i+3))
  
  # Get links of senators from that state
  senator.locs <- which(senate_df$state == state)
  listOfUris <- list(senate_df[senator.locs, 'api_uri'])
  
  return(listOfUris)
}


senate_df$api_uri <- as.character(senate_df$api_uri)

# Write a function that loops through senate_df, grabs the api_uri, makes an API call, extracts the bills_sponsored, bills_cosponsored, and missed_votes_pct
# And append it to the senate_df data frame in a set of new columns



for(i in 1:nrow(senate_df)){
  #print(i)
  api_get <- GET(senate_df$api_uri[i], add_headers(.headers = propublica.key), content_type_json())
  api_parsed <- content(api_get, 'parsed')
  tryCatch( senate_df$bills_sponsored[i] <- api_parsed$results[[1]]$roles[[1]]$bills_sponsored,
           error = function(e) {senate_df$bills_sponsored[i] <- NA})
  tryCatch(  senate_df$bills_cosponsored[i] <- api_parsed$results[[1]]$roles[[1]]$bills_cosponsored,
            error = function(e) {senate_df$bills_cosponsored[i] <- NA})
  tryCatch(  senate_df$missed_votes_pct_previous[i] <- api_parsed$results[[1]]$roles[[2]]$missed_votes_pct,
             error = function(e) {senate_df$missed_votes_pct_previous[i] <- NA})
}

senate_quant <- senate_df[, c("id", "dw_nominate" , "seniority" ,"total_votes", "missed_votes", "total_present", "missed_votes_pct", 
                              "votes_with_party_pct", "bills_sponsored", "bills_cosponsored", "missed_votes_pct_previous")] 

senate_quant_mod <- lm(data = senate_quant, votes_with_party_pct ~ dw_nominate + seniority + total_votes + missed_votes + 
                         total_present + missed_votes_pct + bills_sponsored + bills_cosponsored + missed_votes_pct_previous)

## Perform variable selection using regsubsets and leaps. Try with forward and exhaustive methods. 
## Make a correlation matrix, using cor() I believe
## Run a linear regression model predicting votes_with_party_pct from all variables
## Run a second model using one that you obtained from regsubsets
senate_quant <- senate_df[, c("id", "dw_nominate" , "seniority" ,"total_votes", "missed_votes", "total_present", "missed_votes_pct", 
                              "votes_with_party_pct", "bills_sponsored", "bills_cosponsored", "missed_votes_pct_previous")]


## Perform variable selection using regsubsets and leaps. Try with forward and exhaustive methods.
library(leaps)

regsubsets.out <-
  regsubsets(dw_nominate ~ ., 
             data = senate_quant[,!colnames(senate_quant) %in% c('id')],
             nbest = 2,       # 2 best model for each number of predictors
             method = "forward")

summary.out <- summary(regsubsets.out)
summary.out

plot(regsubsets.out, scale = "adjr2", main = "Adjusted R^2")
plot(regsubsets.out, scale = "bic", main = "BIC")
plot(regsubsets.out, scale = "Cp", main = "Cp")
plot(regsubsets.out, scale = "r2", main = "R^2")




## Make a correlation matrix, using cor() I believe
senate_quant$seniority <- as.numeric(senate_quant$seniority)
cor(senate_quant[,!colnames(senate_quant) %in% c('id')])

## NA's. Two options: 1) remove them or 2) impute them
summary(senate_quant)

## Impute
median_dw <- median(senate_quant$dw_nominate, na.rm=TRUE)
na_locs <- which(is.na(senate_quant$dw_nominate))
na_locs <- is.na(senate_quant$dw_nominate)

senate_quant$dw_nominate[na_locs] <- median_dw

cor(senate_quant[,!colnames(senate_quant) %in% c('id')])

mean_missed_votes <- mean(senate_quant$missed_votes_pct_previous, na.rm = TRUE)
na_locs <- which(is.na(senate_quant$missed_votes_pct_previous))
senate_quant$missed_votes_pct_previous[na_locs] <- mean_missed_votes

pairs(senate_quant[,!colnames(senate_quant) %in% c('id')])


## Run a linear regression model predicting votes_with_party_pct from all variables
senate_quant_mod <- lm(votes_with_party_pct ~ dw_nominate + seniority + total_votes + missed_votes + total_present + missed_votes_pct + bills_sponsored + bills_cosponsored + missed_votes_pct_previous, data = senate_quant)

senate_quant_mod <- lm(votes_with_party_pct ~ ., data = senate_quant[,!colnames(senate_quant) %in% c('id')])
                       
                       
                       ## Run a second model using one that you obtained from regsubsets
                       best.mod <- lm(dw_nominate ~ total_present + bills_sponsored + bills_cosponsored + votes_with_party_pct + missed_votes_pct_previous, data = senate_quant)
                       

votes_uri <- as.character(GetYourSenatorsAPI(address)[[1]][1])

votes_get <- GET(votes_uri, add_headers(.headers = propublica.key), content_type_json())
parsed_votes <- content(votes_get, 'parsed')

str(parsed_votes$results)



# Linear Regression
lm.mod <- lm(votes_with_party_pct ~ ., data = senate_df_quant)
summary(lm.mod)

# Variable selection
library(leaps)


regsubsets.out <-
  regsubsets(votes_with_party_pct ~ ., 
             data = senate_df_quant,
             nbest = 2,       # 2 best model for each number of predictors
             method = "exhaustive")
regsubsets.out
summary.out <- summary(regsubsets.out)
summary.out

best.mod <- lm(dw_nominate ~ total_present + votes_with_party_pct + bills_sponsored + bills_cosponsored + missed_votes_pct_previous, data = senate_quant)
best.mod.quad <- lm(dw_nominate ~ total_present + I(total_present^2) + votes_with_party_pct + I(votes_with_party_pct^2) + bills_sponsored + bills_cosponsored + missed_votes_pct_previous, 
                    data = senate_quant)
