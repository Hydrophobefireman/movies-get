((() => {
    window.getTime = () => {
        const t = (new Date()).getTime() || +(new Date());
        return (t / 1000)
    }
    window.check_data = (tp) => {
        const $ = {
            all: 'all_results',
            player: 'player'
        };
        const $item = $[tp];
        if (!$item) {
            return null;
        };
        const item = window.localStorage.getItem($item);
        if (!item) {
            return null;
        } else {
            try {
                const data = JSON.parse(item);
                if ((data.stamp - getTime()) > (86400 * 1)) {
                    console.log("Old Results")
                    window.localStorage.removeItem($item);
                    return null
                } else {
                    console.log("Found Data in Cache")
                    return data.data
                }
            } catch (e) {
                console.warn(e);
                return null
            }
        }

    }
}))()