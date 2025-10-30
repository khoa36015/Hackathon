export const getProvinceData = async (url, storageKey = 'provinceData') => {
    const cached = localStorage.getItem(storageKey);
    if (cached) {
        return JSON.parse(cached);
    }

    const res = await fetch(url);
    if (!res.ok) {
        throw new Error('Failed to fetch province data');
    }

    const data = await res.json();
    localStorage.setItem(storageKey, JSON.stringify(data));
    return data;
}