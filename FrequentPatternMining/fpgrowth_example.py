#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# $example on$
from pyspark.mllib.fpm import FPGrowth
# $example off$
from pyspark import SparkContext

if __name__ == "__main__":
    sc = SparkContext(appName="FPGrowth")
    fw=open('result.txt','w')
    # $example on$
    freq=[]
    data = sc.textFile("./bracket.txt")
    transactions = data.map(lambda line: line.strip().split(','))
    model = FPGrowth.train(transactions, minSupport=0.13, numPartitions=10)
    result = model.freqItemsets().collect()
    for fi in result:
        
        if len(fi.items)>2:
            #freq+=[(fi.freq,fi.items)]
        	fw.write(str(fi.freq)+","+(",".join(fi.items))+"\n")
    # $example off$
    # freq=sorted(freq)
    # for k,v in freq:
    #     print(k)
    #     print(v[0])
    #     fw.write(str(k)+","+v[0]+"\n")
    # fw.close()
