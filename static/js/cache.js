class CacheData {
    constructor() {
        this.__regex__ = (term) => new RegExp(`.*?${term}`, 'gm');
        this._cachename = 'cached_terms';
        this.getcache = (cachename = this._cachename) => {
            const data = localStorage.getItem(cachename);
            if (data) {
                return JSON.parse(data)
            } else {
                return data
            }
        };
        this.removecache = (cachename = this._cachename) => {
            localStorage.removeItem(cachename)
        };
        this.populate_cache = (tocache, cachename = this._cachename) => {
            let _cache;
            if (typeof tocache === 'object') {
                _cache = JSON.stringify(tocache)
            } else {
                _cache = tocache;
            }
            const data = {
                cache: _cache,
                stamp: new Date().getTime()
            };
            window.localStorage.setItem(cachename, JSON.stringify(data))
            return !0;
        }
        this.__test__ = (val, text) => {
            return this.__regex__(val).test(text);
        }
        this.get_search_results = function (val, data, attr = 'movie') {
            /*val:string,test:array*/
            const ret = [];
            for (const b of data) {
                if (this.__test__(val, b[attr])) {
                    ret.push(b)
                }
            }
            return ret
        }
    }
}

function ok() {
    return 'k'
}