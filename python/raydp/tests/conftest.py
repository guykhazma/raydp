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

import logging

import pytest
from pyspark.sql import SparkSession
import ray


def quiet_logger():
    py4j_logger = logging.getLogger("py4j")
    py4j_logger.setLevel(logging.WARNING)

    koalas_logger = logging.getLogger("koalas")
    koalas_logger.setLevel(logging.WARNING)


@pytest.fixture(scope="function")
def spark_session(request):
    spark = SparkSession.builder.master("local[2]").appName("RayDP test").getOrCreate()
    request.addfinalizer(lambda: spark.stop())
    quiet_logger()
    return spark


@pytest.fixture(scope="function")
def ray_cluster(request):
    ray.init(include_java=True, redis_password="123")
    request.addfinalizer(lambda: ray.shutdown())
