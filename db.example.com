$TTL 3600
@    IN SOA ns1.example.com. admin.example.com. (
        2024110901 ; Serial
        3600       ; Refresh
        1800       ; Retry
        604800     ; Expire
        86400      ; Minimum TTL
)
@    IN NS ns1.example.com.
ns1  IN A 192.0.2.1
@    IN A 192.0.2.1

; RESINFO records
@ 3600 IN RESINFO qnamemin exterr=15-17 infourl=https://resolver.example.com/guide
* 3600 IN RESINFO qnamemin exterr=15-17 infourl=https://resolver.example.com/guide
