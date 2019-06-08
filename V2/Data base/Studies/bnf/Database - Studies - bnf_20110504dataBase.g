grammar DataBase;

String		: (CharLow 
		| CharUpp
		| CharNum
		| CharEsp)
		;
CharEsp		: ' ';
SpecialChar	: '0x7c';
EOL		: '\r' '\n' | '\n';
CharLow		: 'a'..'z';
CharUpp		: 'A'..'Z';
CharNum		: '0'..'9';
CharPonc	: ',' | '.' | '?' | ';' | '.' | ':' | '/' | '(' | ')'
		;
ColumnValue	: (String | CharNum | SpecialChar)*;

ColumnName	: String ;

TableStruct	: TableHeader TableBody;

TableHeader	:  ColumnName ColumnSep TableHeader 
		| ColumnName EOL
		;
TableBody	:  ColumnValue ColumnSep TableBody 
		| ColumnValue EOL
		;

ColumnSep	: '||'
		;