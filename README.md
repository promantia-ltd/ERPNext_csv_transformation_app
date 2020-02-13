## Csv Transformation

Map the files csv files into the erpnext templates


#### Usage
First install the app

To execute:

bench --site <site_name> execute csv_transformation.basic_transform.transform.transformFile --kwargs {'filePath' :'<"your main csv file path">','dataType':'<"type of data you want to transform">'}

    Example
    
    
        bench --site site1.local execute csv_transformation.basic_transform.transform.transformFile --kwargs "{'filePath'    :'home/paul/erpNext/frappe-bench/apps/csv_transformation/csv_transformation/basic_transform/data/item-master.csv','dataType':'item-data'}"


#### License

MIT
