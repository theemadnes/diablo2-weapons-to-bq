# diablo2-weapons-to-bq

With the recent remastered (and resurrected!) re-release of [Diablo 2](https://diablo2.blizzard.com/en-us/), I put together a hello world to do some lightweight data transforms (via a Python script) and then import [D2 weapons data](https://raw.githubusercontent.com/blizzhackers/d2data/master/json/weapons.json) (although it could be any of the data) to BigQuery and explore the data. 

I'm using us-central1 as my region, and using the `bq` CLI tool to interact with BigQuery.

The source of this data is Blizzhacker's [awesome GitHub repo](https://github.com/blizzhackers/d2data).

### Setup 

*pull down the json*

```
wget https://raw.githubusercontent.com/blizzhackers/d2data/master/json/weapons.json
```

Before this JSON data can be uploaded to BQ, we need to do a little data prep. In this repo is a use-case specific data prep script (i.e. hardcoded for this specific data) that will do things like:
- Convert to [JSONL format](https://hackernoon.com/json-lines-format-76353b4e588d)
- Make sure the keys in the JSON (which will be used as column names) conform to BQ's requirements, so replace spaces with `-` and prefix keys with numeric characters at the beginning with `-`

run the data prep script
```
python3 d2_json_to_jsonl.py # outputs weapons.jsonl
```

*create a BQ dataset*

```
# set project ID
export PROJECT_ID=YOUR_PROJECT_ID

bq --location=us-central1 mk \
--dataset \
--description "fun with D2 data in BQ" \
${PROJECT_ID}:diablo2
```

*import the JSONL data*

```
bq load --autodetect \
--source_format NEWLINE_DELIMITED_JSON \
${PROJECT_ID}:diablo2.weapons weapons.jsonl 
```

### Explore the data

Now that the data has been loaded, feel free to try some queries to explore the data. I like just using the BQ console for this as the Explorer is nice.

*What are the 10 most expensive weapons?*
```
SELECT name, cost 
FROM diablo2.weapons
ORDER BY cost DESC
LIMIT 10;
```

or.... 

*Per weapon type, what's the most expensive item cost?*
```
SELECT type, MAX(cost) as max_cost
FROM diablo2.weapons
GROUP BY type
ORDER BY type;
```

```
SELECT name, cost, weapons.type
FROM diablo2.weapons
INNER JOIN (SELECT type, MAX(cost) as max_cost
FROM diablo2.weapons
GROUP BY type
ORDER BY type) AS max on max.type = weapons.type
AND max.max_cost = weapons.cost
ORDER BY weapons.type;
```