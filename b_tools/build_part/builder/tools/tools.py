def transformId(idToTransform:str, bracelets:bool = False) -> str:
        res = ''.join(idToTransform.split('-'))
        try:
            int(res[0])
        except:
            pass
        else:
            res = res.replace(res[0], 'a', 1)
        if not bracelets:
            return res
        else:
            return '"'+res+'"'