alter table file_records
    add _id bigint generated always as identity;

alter table file_records
    add constraint file_records_pk
        primary key (_id);

delete from file_records
where file_key = 0;

delete from file_records
where file_key not in (SELECT file_id FROM files);

delete from records
WHERE record_id not in (SELECT record_key FROM file_records);

alter table records
    alter column record_offset set default 0;

alter table device_properties
    add _id bigint generated always as identity;

alter table device_properties
    add constraint device_properties_pk
        primary key (_id);
