db-str		= line-col EOL 1*(line-val EOL); a table begins with colmns names (first line
line-col	= 1*(col-name col-delim)
line-val	= 1*(col-val col-delim)
col-name	= %x41-5A col-name / %x61-7A col-name / %x41-5A / %x61-7A
col-delim	= %x7C %x7C
col-val		= (%x20-7B / %x7D-7E) col-val / %x20-7B / %x7D-7E
EOL		= (%x0D %x0A) / %x0A
