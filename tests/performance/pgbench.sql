INSERT INTO sensor_snapshot(id, measuredproperty, value, geom)
VALUES (md5(random()::text), 'temp', random()*100, ST_SetSRID(ST_MakePoint(0,0),4326));
