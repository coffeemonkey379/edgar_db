# edgar_db
Upload SEC 13-F files to searchable SQLAlchemy ORM database - only tested with PostgresSQL.

Takes the files stored as zip files this SEC [webpage (https://www.sec.gov/dera/data/form-13f)] 
and uploads to a searchable database.

The database tables and naming convention are based on the details in 'FORM13F_readme.htm'.

# To-Do List
- Complete mapping from file to database table (only SUBMISSION.tsv) completed so far.
- Complete unit tests & documentation.
- Test other database back-ends.
- Add additional table to determine if file has been uploaded previously.

