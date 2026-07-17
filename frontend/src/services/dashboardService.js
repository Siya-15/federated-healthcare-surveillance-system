import api from "./api";

export const getStatistics = async () => {
    const response = await api.get("/statistics");
    return response.data;
};

export const getAlerts = async () => {
    const response = await api.get("/alerts");
    return response.data;
};

export const getEmergingSymptoms = async () => {
    const response = await api.get("/emerging-symptoms");
    return response.data;
};