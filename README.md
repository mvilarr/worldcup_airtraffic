# An Analysis of Air Traffic During the FIFA World Cup

The initial idea for this project was to analyze how air traffic changed across the 16 host cities during the 2026 FIFA World Cup in the United States, Canada, and Mexico. I then realized that this would involve an overwhelming amount of data, so I narrowed the scope to New York, which is hosting eight matches, including the final, and is home to the tournament's largest stadium, in New Jersey.

My main finding was the opposite of what I had expected: the FIFA World Cup did not significantly change air traffic. There was only a marginal increase of less than 2%, or approximately 700 additional flights, compared with the same period in the previous year, when the United States hosted the FIFA Club World Cup, between June 14 and July 13.

## Collecting the Data
### FIFA Match Data

The most challenging part of this project was obtaining the data. First, I needed information about the match dates, the teams playing, and the host cities and stadiums. I tried scraping FIFA's website using BeautifulSoup, XPath, and Selenium, but I was unsuccessful. BeautifulSoup did not work because the website is dynamic, and I believe I was not selecting the correct elements when using XPath. Selenium caused my computer to crash. https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums

The solution was to find another website where this information was easier to collect. I found one that provides a downloadable table that can be imported directly with pandas. Before finding this source, I downloaded FIFA's official schedule in PDF format and attempted to extract the data using the Natural PDF library, but I could not fully understand the documentation. https://www.zoho.com/toolkit/fifa-world-cup-2026.html?zredirect=f&zsrc=langdropdown&lb=pt-br&lb=pt-br

### Flight Data

I then needed to collect flight data. The OpenSky API was the only free API I could find that provided recent information on flights arriving at New York City's airports. Most of the alternatives were paid services. I used the OpenSky API, which provides flight data by airport. https://openskynetwork.github.io/opensky-api/ 

Although the documentation mentions an official Python library, I installed it and found that it did not work properly. I contacted the maintainers through their Discord community and was informed that the library had not been maintained for a long time. As a result, I had to work directly with the API.

Using the API requires creating an account and obtaining credentials, and there is a limit of 4,000 credits per day. I collected data from New York City's three major airports: JFK, LaGuardia, and Newark. After retrieving the 2026 data, I exceeded the daily credit limit on my first account and had to create a second set of credentials to collect the 2025 data.

Another limitation of the API is that flight data can only be retrieved within two-day intervals. Therefore, I had to write a loop to collect data covering an entire month. The dates also had to be converted into Unix time, which represents the number of seconds since January 1, 1970. I created both a function and a loop to handle the API requests automatically.

## Analysis

I analyzed the first three weeks of the tournament, as well as the week preceding its opening (June 6 to July 5 in both 2025 and 2026). This period was chosen to capture tourists and fans arriving before the competition began—possibly to spend time in the city—as well as the period leading up to July 5, the date of New York City's last World Cup match before the final, which is scheduled for July 19, 2026.

I attempted to identify patterns in the days leading up to each match by considering only flights that arrived up to four hours before kickoff. However, I did not find any meaningful trends.

I also analyzed where the flights originated and found that the overwhelming majority were domestic flights from within the United States. Another filter focused on flights arriving from Brazil, but they represented only about 10% of the dataset and did not increase during the World Cup period—not even around the dates when Brazil played in New York City (against Morocco on June 13 and Norway on July 5).

## Reflections

One of the biggest challenges of this project was narrowing down the original idea and working around the limitations of the API. It was also difficult to write about the findings because the results were not particularly dramatic, it just showed that the air traffic didn't change much. Additionally, scraping the data and creating the visualizations in Flourish proved challenging, because it was my first time using the platform and also the data itself did not reveal many significant patterns.

Despite these challenges, I learned a great deal throughout the process. It was my first time working with an API that requires credentials to be validated in order to obtain an authentication token before making requests. It was also my first experience writing functions specifically designed to interact with an API.

