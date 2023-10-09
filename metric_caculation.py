from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
EPS = np.finfo(np.float64).eps


def calc_cbm_score(t1_idx, t2_idx) -> float:
    t1 = SELECTED_ESCO_SPANS[int(t1_idx)]
    t2 = SELECTED_ESCO_SPANS[int(t2_idx)]

    t1_count = SPANS_DOCS_COUNT[t1]
    t2_count = SPANS_DOCS_COUNT[t2]
    t1t2_count = 0
    for doc in DOCS_SPANS:
        if t1 in doc and t2 in doc:
            t1t2_count += 1

    if t1_count == 0 or t2_count == 0:
        return 0.
    elif t1_count == t2_count and t1_count == t1t2_count:
        return 1.
    else:
        # print(t1_count, t2_count, t1t2_count, np.log10(t1_count + 1), np.log10(t2_count + 1), np.power(np.log10(t1t2_count) + EPS, 2))
        # np.power(np.log10(t1t2_count), 2)
        return np.power(np.log10(t1t2_count + 1), 2) / (np.log10(t1_count + 1.) * np.log10(t2_count + 1.))


CBM_SCORES = pairwise_distances(np.arange(len(SELECTED_ESCO_SPANS)).reshape((-1, 1)), metric=calc_cbm_score, n_jobs=-1)
CBM_SCORES
COS_SIMS = cosine_similarity(list(get_embedding(span) for span in SELECTED_ESCO_SPANS))
# calc_cbm_score(0, 1)