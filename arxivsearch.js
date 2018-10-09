const axios = require('../../utils/axios');
const cheerio = require('cheerio');
const config = require('../../config');

module.exports = async (ctx) => {
    const query = ctx.params.query;
    const url = `https://arxiv.org/search/?searchtype=abstract&query=${query}&size=50&order=-announced_date_first`;
    const response = await axios({
        method: 'get',
        url: url,
        headers: {
            'User-Agent': config.ua,
            Referer: 'https://arxiv.org',
        },
    });

    const data = response.data;

    const $ = cheerio.load(data);
    const list = $('ol > li');
    const resultItem = [];
    for (let i = 0; i < list.length; i++) {
        const item = {
            title: '',
            description: '',
            link: '',
        };
        const data = $(list[i]);
        const key = data.find('.title.is-5.mathjax').text();
        const value = await ctx.cache.get(key);
        if (!value) {
            item.link = data.find('div > p > a').attr('href');
            item.title = key;
            item.description = data.find('.abstract-full.has-text-grey-dark.mathjax').text();
            resultItem.push(item);
        }
    }

    ctx.state.data = {
        title: `arxiv ${query}`,
        link: 'https://arxiv.org',
        description: 'arxiv search',
        item: resultItem,
    };
};
