klient_price = '''
select 
  case when ta.inn is not null then ta.name else tk.name end as "Контрагент", 
    --группировать по idsystem
  case when t2.idsystem = 11 then 'WHost'
     when t2.idsystem = 12 then 'Fort'
     when t2.idsystem = 13 then 'GSoft'
     when t2.idsystem = 14 then 'Scout'
     when t2.idsystem = 15 then 'Era'
     when t2.idsystem = 16 then 'WLocal'
     else ''
     end,
  t2.object

from tdata t2
left join twialon100 tw on tw.logintd = t2.login
left join tklient tk on tk.id = tw.tkid
left join ttarif tt on tt.id = 
    (select tt1.id from ttarif tt1 where tt1.tkid = tk.id and t2.dimport between tt1.dbeg and tt1.dend LIMIT 1)
left join tagat ta on ta.idsystem = t2.idsystem and ta.idobject = t2.idobject and t2.dimport between ta.dbeg and ta.dend

where t2.isactive = ' Да'
and tk.inn is not null
--and t2.dimport = (SELECT max(tdata.dimport) AS max FROM tdata)
--автоматически предыдущий день
and t2.dimport = (SELECT max(tdata.dimport) AS max FROM tdata)
and upper(t2.object) not like '%ТЕСТ%'
and not (upper(t2.object) like '%TEST%' and upper(t2.object) not like '%MICROTEST%')
and upper(t2.object) not like '%ПРИОСТ%'
and upper(t2.object) not like '%ППРО%'
and upper(t2.object) not like '%НОВТ%'
and not (upper(t2.object) like '%ПЕРЕ%' and t2.idsystem in (11,16))
and not (upper(t2.login) like '%ТЕСТ%' and t2.idsystem in (15))
and tk.id not in (2752, 1925, 3287)
order by 1
'''
