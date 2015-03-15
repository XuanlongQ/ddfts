
BEGIN {
     highest_flow_id = 0;
}
{
   action = $1;
   time = $2;
   from = $3;
   to = $4;
   type = $5;
   pktsize = $6;
   flow_id = $8;
   src = $9;
   dst = $10;
   seq_no = $11;
   packet_id = $12;

   if ( flow_id > highest_flow_id )
     highest_flow_id = flow_id;

   if ( start_time[flow_id] == 0 )  
    start_time[flow_id] = time;

   #if ( action != "d" ) {
   #   if ( action == "r" ) {
   #      end_time[flow_id] = time;
   #   }
   #} else {
   #   end_time[flow_id] = -1;
   #}
   if ( action == "r" ) {
      end_time[flow_id] = time;
    }else {
      end_time[flow_id] = -1;
    }
}                             
END {
    for ( flow_id = 0; flow_id <= highest_flow_id; flow_id++ ) {
       start = start_time[flow_id];
       end = end_time[flow_id];
       packet_duration = end - start;

       #if ( start < end ) printf("%f %f\n", start, packet_duration);
       if ( start < end ) printf("%d\t%f\n", flow_id, packet_duration);
   }
}
