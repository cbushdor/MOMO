package packages::Time;

# +-------------------------------+
# | Dorey Sebastien               |
# | Daemon.pm                       |
# | Written on August 8 th 2005   |
# | Last update on Sept 19th 2005 |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( dates_substracted  are_dates_greater  are_dates_smaller   are_dates_equal 
	      print_res          test_for_smaller   test_for_greater    test_for_equal
	      get_formated_date
	      );
@EXPORT_OK = qw( timegm_nocheck timelocal_nocheck );
