from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glueContext = GlueContext(sc)

print("ClaimsIQ Bronze to Silver ETL Started")



