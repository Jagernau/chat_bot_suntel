from datetime import date
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

detail_klient = '''
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

where (tk.name like 'XXX' or tk.name like '%XXX%' or tk.name like upper('%XXX%') or tk.name like INITCAP('%XXX%') or upper(ta.name) like '%XXX%' or ta.name like 'XXX' or ta.name like '%XXX%' or ta.name like upper('%XXX%') or ta.name like INITCAP('%XXX%') or upper(ta.name) like '%XXX%' )

and t2.isactive = ' Да'
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

show_chenge_objects_to_day = f'''
select login, object, idsystem from tdata
where dimport = (SELECT max(dimport) FROM tdata)
EXCEPT
select login, object, idsystem from tdata
WHERE dimport = (SELECT CAST(MAX(dimport) - INTERVAL '1' DAY AS TIMESTAMP WITHOUT TIME ZONE) FROM tdata)

'''
klient_price_with_mail = '''
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
  t2.object, tm.email

from tdata t2
left join twialon100 tw on tw.logintd = t2.login
left join tklient tk on tk.id = tw.tkid
left join ttarif tt on tt.id = 
    (select tt1.id from ttarif tt1 where tt1.tkid = tk.id and t2.dimport between tt1.dbeg and tt1.dend LIMIT 1)
left join tagat ta on ta.idsystem = t2.idsystem and ta.idobject = t2.idobject and t2.dimport between ta.dbeg and ta.dend

left join temail tm on tm.inn = (case when ta.inn is not null then ta.inn else tk.inn end) 
							    and case when tm.kpp is null and (case when ta.inn is not null then ta.kpp else tk.kpp end) is null then true 
								else tm.kpp = (case when ta.inn is not null then ta.kpp else tk.kpp end) end

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

all_db_object_today = '''

select object from tdata
where dimport = (SELECT max(dimport) FROM tdata)
and idsystem = XXX

'''

abonents_object = '''
select 
  case when ta.inn is not null then ta.name else tk.name end as "Контрагент", 
  t2.object

from tdata t2
left join twialon100 tw on tw.logintd = t2.login
left join tklient tk on tk.id = tw.tkid
left join tagat ta on ta.idsystem = t2.idsystem and ta.idobject = t2.idobject and t2.dimport between ta.dbeg and ta.dend


where t2.isactive = ' Да'
and tk.inn is not null
--and t2.dimport = (SELECT max(tdata.dimport) AS max FROM tdata)
--автоматически предыдущий день
and t2.dimport = (SELECT max(tdata.dimport) AS max FROM tdata)
and t2.idsystem = XXX

and upper(t2.object) not like '%ТЕСТ%'
and not (upper(t2.object) like '%TEST%' and upper(t2.object) not like '%MICROTEST%')
and upper(t2.object) not like '%ПРИОСТ%'
and upper(t2.object) not like '%ППРО%'
and upper(t2.object) not like '%НОВТ%'
and not (upper(t2.object) like '%ПЕРЕ%' and t2.idsystem in (11,16))
and not (upper(t2.login) like '%ТЕСТ%' and t2.idsystem in (15))
and tk.id not in (2752, 1925, 3287)
'''


