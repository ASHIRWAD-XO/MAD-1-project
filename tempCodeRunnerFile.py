r=Requests(sname=sname.sname,iname=iname.iname,campaign_id=cid,scheck=value)
            db.session.add(r)
            db.session.commit()