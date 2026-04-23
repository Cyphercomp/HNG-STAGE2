# **PROFILE API**
 Is a api that create  profiles using external profile and it create a profile using *name* provided in the query and it finds the highest gender probability of that *name* and the highest country probability of that name.

You can query this profile through this endpoint  
_hng-stage2-production-c503.up.railway.app/api/profiles/_


## **FILTERS** 
This API can filter the data using the following fields 
* gender : _api/profiles/?gender=value_
* age_group: _api/profiles/?age_group=value_
* country_id: _api/profiles/?country_id=value_
* min_age: _api/profiles/?min_age=value_
* max_age: _api/profiles/?max_age=value_
* min_gender_probability: _api/profiles/?min_gender_probability=value_
* min_country_probability: _api/profiles/?min_country_probability=value_

    youcan also query a combined filter query using the following 
    query: _http://127.0.0.1:8000/api/profiles/?gender=female&age_group=senior&country_id=TZ&age__gte=60&age__lte=70&gender_probability__gte=0.6&country_probability__gte=0.6_

## **SORTING**
The API also support sorting either Ascending or Descending Using the following fieds: 
* age: _api/profiles/?sort_by=age=value&order=value_
* created_at: _api/profiles/?sort_by=created_at=value&order=value_
* gender_probability: _api/profiles/?sort_by=gender_probability=value&order=value_

The order Value can take either **asc** for Ascending or **desc** for Descending sorting 

## PAGINATION 
The API also return paginated data and you can specify the page number by using **/?page=value** you want and number of data to be returned by using **/?limit=value**

