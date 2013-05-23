# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import orm
from reddwarf.configuration.models import DBConfiguration
from reddwarf.configuration.models import DBConfigurationItem

from reddwarf.db.sqlalchemy.migrate_repo.schema import create_tables
from reddwarf.db.sqlalchemy.migrate_repo.schema import DateTime
from reddwarf.db.sqlalchemy.migrate_repo.schema import drop_tables
from reddwarf.db.sqlalchemy.migrate_repo.schema import Integer
from reddwarf.db.sqlalchemy.migrate_repo.schema import String
from reddwarf.db.sqlalchemy.migrate_repo.schema import Table

meta = MetaData()

configuration = Table(
    'configuration',
    meta,
    Column('id', String(36), primary_key=True, nullable=False),
    Column('name', String(64)),
    Column('description', String(256)),
    Column('tenant_id', String(36))
)

configuration_items = Table(
    'configuration_item',
    meta,
    Column('configuration_id', String(36), ForeignKey("configuration.id"),
           nullable=False),
    Column('configuration_key', String(128), nullable=False, primary_key=True),
    Column('configuration_value', String(128))

)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    create_tables([configuration])
    create_tables([configuration_items])

    instances = Table('instances', meta, autoload=True)
    instances.create_column(Column('configuration_id', String(36),
                                   ForeignKey("configuration.id")))


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    drop_tables([configuration])
    drop_tables([configuration_items])

    instances = Table('instances', meta, autoload=True)
    instances.drop_column('configuration_id')
