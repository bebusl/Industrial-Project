const celery = require("celery-node");
const { create } = require("../model/user");

const client = celery.createClient("amqp://localhost", "redis://", "general");
const analysis_client = celery.createClient("amqp://localhost", "redis://", "analysis");

async function get_booklist(searchKeyword) {
    const task = client.createTask("tasks.multi");
    const result = task.applyAsync([searchKeyword]);
    const data = await result.get();
    return data;
}

async function get_reviews(itemId) {
    const task = client.createTask("tasks.crawl");
    const result = task.applyAsync([itemId]);
    const data = await result.get();
    return data;
}

async function get_keywords(books) {
    const task = analysis_client.createTask("analysis-task.analysis_");
    const result = task.applyAsync([books]);
    const data = await result.get();
    return data;
}

module.exports = { get_booklist: get_booklist, get_reviews: get_reviews, get_keywords: get_keywords };
