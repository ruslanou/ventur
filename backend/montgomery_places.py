"""
Montgomery, Alabama — Ventur Places Dataset
Real places curated for the Ventur hackathon demo.
Load this into ChromaDB for RAG-powered AI recommendations.
"""

MONTGOMERY_PLACES = [
    # ── RESTAURANTS ──────────────────────────────────────────────
    {
        "id": "rest_001",
        "name": "Central Restaurant",
        "category": "Restaurant",
        "subcategory": "Farm-to-Table",
        "address": "129 Coosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Montgomery's premier farm-to-table dining experience. Chef-driven menu featuring locally sourced Alabama ingredients. Known for their Southern-inspired dishes with a modern twist. Perfect for date nights and special occasions.",
        "hours": "Tue-Sat 5pm-10pm",
        "price_range": "$$$",
        "points": 200,
        "photo_ref": "ATCDNfWS2ecRzd4BLKlgUbqHChXdqevdHEOoTIa54G5e5hXSBLS0Xh2Rd6aZOrVSQOPofjn6a7pRDAu4XYXKNLhCmz8FW-4o1KQMP7EgGipd_0UQTRmIUoxRUsyFyMKlYcSqwIKH5frVohB8zWoXQMT1bfIFqitaZ7jjJ0HuKHutj_yIDb4A_LxX13Wu1ulSuCMzZBqak07RTS0TCSnzKXmF2kBBX6Sr4IaDLjgvNTqEs01ewOtim9y9GE9ieLcZze1KWb96CmmsrLMngVh2bqXIlFSi1jSUee3THAUejF1IJEwoIIO_MJa7ojYlQKt32fHOqWnYLM7D-A1YH4gRdXIv0dc_Il0j5iBOz4nO0aL1nFwXcJyiGVbSQ5WRpI5sYFotQTuQVf5F-LoiqdQds7-Pi163em0Y-1LU_GtMjX3eYo7SY6hdGPfDx3hmqL11LBOO6uZAQMri2r9qTaAtN2TgP1kwqZhVh_VH531NDgm4xkoEytiiP_TwTQ6IdMOmtSU7G_OyaJ1yMeZXKyrhyDvc08aXa7Mi3sjGiVDCiNj1DS9rImO_hCx1-00H22sTh3vUfhNi13_N",
        "tags": ["upscale", "southern", "farm-to-table", "date night", "downtown"],
    },
    {
        "id": "rest_002",
        "name": "Dreamland BBQ",
        "category": "Restaurant",
        "subcategory": "BBQ",
        "address": "101 Tallapoosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Legendary Alabama BBQ institution since 1958. Famous for their slow-smoked ribs, pulled pork, and homemade sauce. A Montgomery must-visit that locals swear by. James Beard recognized Alabama BBQ culture.",
        "hours": "Mon-Sun 11am-9pm",
        "price_range": "$$",
        "points": 150,
        "photo_ref": "ATCDNfWAUMmjvDRT60NvcxEigDX4PmK-k73aVIvefjHhVQrtJx9EQB2AdIu4qVTW40OiqsirMSIYHA3_Tm19a26kQJxu5dt7C8pKBDukvr6ZpH6-dSpIjDqsR5tWKI_U7Lomm7nbkmB6-eTjWxT-jyJF1JRfaKc2tfj0t4LbeYisyYXVR6CwM9D1sUqQFm8FcGSiLsjNRYr5Fvvg_cgSvMH-tpgfcI0_EH4blRGIZ73dcudwO-8xKsOk5F7myg0QeunM5go467_qEzzB7D6QDyd-ML9DbWvae0OYBO181bILJT9l0WIOc2EiU0Eaezw48Vup2FPDgLi76dpQzjaWtf4rYaeb89798-_PrK699DIG0PNmEWf2McLzH4wm76gK9L1o7bzX50W9kAyNAEUECmAk2TQmlzj83shUxE4e9ZVrm9NCZRf16EAFXEcnI5bkiSFdGGbbE0-TBjetr0SO8anizg3ELzjVqN4Rh2sndhtG9cBChMEw_rBOmTkUFuwcsR8Ihi0WsNhfvsXhY3xvs-qbtqY0zkEbZ8FSGb_xkPUfgpTFGK0VYCwGOJvwslT4aIjoHMsc6187",
        "tags": ["bbq", "ribs", "casual", "iconic", "family-friendly", "lunch", "dinner"],
    },
    {
        "id": "rest_003",
        "name": "Vintage Year Restaurant",
        "category": "Restaurant",
        "subcategory": "Fine Dining",
        "address": "405 Cloverdale Rd, Montgomery, AL 36106",
        "neighborhood": "Cloverdale",
        "description": "Montgomery's most beloved fine dining restaurant housed in a historic building. Renowned wine list with over 800 selections. Classic American cuisine with European influences. A Montgomery landmark since 1992.",
        "hours": "Tue-Sat 6pm-10pm",
        "price_range": "$$$$",
        "points": 250,
        "photo_ref": "ATCDNfUBlRbHcqrEkiFM6GOxzkM_fFDUwKeIdafuPb57SItLtOYB1cfhVU3yzHkGOM0imAqX1df4dsAKS-kGj5dw83yH1oKWzTwd0zKsO-JOOUu5WP9G0X3ekYg26c87puAaiNHjUNWTdl1N4_kmv8XKZ3kKpk0wn0nbsqjLoAzpkv_sq_masg06lBoIXPAJvSKH39l4-kLE-qEVEclSXCWKJGjAjCErbJVmxTpRoxh9Zb1Jzvt2x0pZ_6duSwEj9OCCa7lAAg_v0u3RlksHOFZokkLcgqdgqck_qHM_FBPebSirDPDQG0-rl7llwslVqsCzDNo75P7sDY9KzQN-xb3ThIE_D1_HrpUBm-CZf42GiqLcyw3mni3GabKBoTOUWpdIrYTe-lF-HgY6SNtTPO88kOTbIJwy95c8-8TRysQy6rOGsHYsKmzyFw6mHlpa1Z5a9d0yFR33TQh1nXV84gAeUk8HBK5hQUFiLM7DNUuZHFsu95B2Ldgf_jvtV0sy6bJhTDdhKpOp0FHhJbQ1xW-h-qge_u7qoAA6vjlVPVku7NjZX7TCTTXwfEZqglaMyPZmYZTRB2LETfWHVA",
        "tags": ["fine dining", "wine", "romantic", "historic", "special occasion"],
    },
    {
        "id": "rest_004",
        "name": "Alley Bar & Kitchen",
        "category": "Restaurant",
        "subcategory": "American",
        "address": "Register Alley, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Beloved downtown spot tucked in historic Register Alley. Known for creative cocktails, burgers, and live music on weekends. The go-to spot for downtown Montgomery nightlife and casual dining.",
        "hours": "Mon-Sun 11am-2am",
        "price_range": "$$",
        "points": 150,
        "photo_ref": "ATCDNfWQvvvzYCP6W5EytwS2Yn41tbwCrNPtz79SpcaeeLTRE0UXeMNuQ_k8LX4xquE0vuND3ADrwQoOIG9B8h3PhnbA9iNqPuSAYtWuTWvZy8CcwrwWGLqlQA-C8wLw64-abOvjZ9XehO-G-2PbJNReUatQUlU_jnDRMhhNhWp47oVYCmSm8wWOxG3eo5cyZxyj-TOHOEnNqgJBPgdcmnfDYh6SvYslf0Z4ZZoUhrQCMAPAWdPaoLq2MwVHOiALfLPn8A2wnaALLMEzb13YHkbPZX6Yin6SSTKoEL_BOSiy7DBpHAAUQ6kqjRHt1i5qbpwMn_sjH8k94PTxyX7XQEdBmAzNdFoc1qaftY6gYgR9y0uKPKouziUvv9wZZLT_6yzbzfGJB63azDPrjxLConDWlOAMIEV6e5dYWS55vS_s23l5ixxitB9quFpf6V4s-Q92olnc9o4wtzD6kwiV_xfxJmx0DzX3QI_A-JevvvYeyriUWQkGTonrghUyGbhdDK5h7gTpVxzEdrJ0Hcx0UBaNDvS7Mjuhpk2gV7luuqvUTNTtltsj3_e4dOxxw4f5SktluNYeIUKOf4GuQQ",
        "tags": ["casual", "burgers", "live music", "nightlife", "cocktails", "downtown"],
    },
    {
        "id": "rest_005",
        "name": "Vintage Café",
        "category": "Restaurant",
        "subcategory": "Café & Brunch",
        "address": "301 Dexter Ave, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Charming café steps from the Alabama State Capitol. Perfect for breakfast and brunch with artisan coffee, fresh pastries, and creative egg dishes. Popular with state workers and tourists exploring downtown.",
        "hours": "Mon-Fri 7am-3pm, Sat-Sun 8am-2pm",
        "price_range": "$",
        "points": 100,
        "photo_ref": "ATCDNfWIm_K4pSlzBsKYmCv5V8Qt-A5lQb57DHyIw2A1hZVlFKy-B8R8_S-aC58O0hhrEiI_n0p79_A2gaBc1kAvInTfho4jfsYjYdYafSqyxGel2U4ek1hPQpOskZx5rzwIqCVdG4iPsWtnocQ_3TpSZdRHG6Avt_dNWcVcSK74aHx4dh5RRadmfLKZdMj_hbK-6KPt_QpOqdVBknu_IYCNyxezfj-9Y89X8qgyzIokDhK_RwUpF2s4xmg9qnhLsxQL1pedq8h2vGKDQ4bmJsWUBTEUi7en5AIKn-zCUMcvXdi31RKApgzBu7bIyT8BftMBJaoYUeMF5ou_2QM7wYNc70RnYIW6T0RAZqzmqCWmat_8myAhz83EaNWZdqmnwXf32ZT4J97VtkmHxQK1QFwdRWP-dASlYpcSPHiL6H56ZcLnjRxat1FcJZtlN06FRCTIgpuAT-JZ95jVkocnYAvD1_L1ZzbFWAfGsKoLzpZE2MhuKQNfWSQTKVSgi7isrmBubNbPenvZJQ-OgAQJMyKjHf6JwgJu9Lw488WxGK93K9YedPGfhtcWL9UGnQ809-iEymG5cw",
        "tags": ["breakfast", "brunch", "coffee", "pastries", "casual", "downtown"],
    },
    {
        "id": "rest_006",
        "name": "True Kitchen & Bar",
        "category": "Restaurant",
        "subcategory": "Contemporary American",
        "address": "359 Dexter Ave, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Contemporary American restaurant and bar in the heart of downtown. Known for creative small plates, craft cocktails, and an impressive happy hour. Great outdoor seating with views of downtown Montgomery.",
        "hours": "Mon-Thu 11am-10pm, Fri-Sat 11am-midnight",
        "price_range": "$$",
        "points": 175,
        "photo_ref": "ATCDNfXo3ofHueDhoG9iuY19mh7T_sqikUh7cF2rGmSdNUo00HUMmdHtUvOGJH07QJx1BMihqVC5yJoPSxQEFVgHSRAqENDNvdkavWj8ZYI_4b2oS84w69o6lioJ0ZaDwmJJ2hql3iOFh5Vik9H0VcCbZNUe0YtBn0bT5PyoMfs1RHB66WrAuqF2Nd65gkZmiCQJ1OyqqaYTPuMurm1HLY5iXFcvkCROH4Mv17K9FZu2mYEBnTUlr7kl3YHzSqon8-RqqeV9t1i1I_FBYNeGvgtAhaPsR7wBmt4wkcITnUHPuW8k2SG3OmkZqQcCFtlTmHABaL15osmrJSmpDgsPP2u2x3sXKoRILSbgmEuFhB946lQ0JqtkzegCADN7JgoWQiTlvSOYb0i4KsKRXB__2l80GVmwOq0j2b0CBWiTtM4n0kzKMl9YmkmFVYFXSvCpg6dFeZmoVBY0dYAq48elhPwOWaQVmA899qWRcMAOWfvtbDnsi_aFXbyupl4iX93jAB_HwT_FHkSuEAcCL--EcpKx0MLs8DSbxuLeYDuycbzYAS6cW5H2dPI0aqsGhGBK65jPY_R_Jw",
        "tags": ["contemporary", "cocktails", "happy hour", "outdoor seating", "downtown"],
    },

    # ── BARS & NIGHTLIFE ──────────────────────────────────────────
    {
        "id": "bar_001",
        "name": "Cahaba Brewing Company",
        "category": "Bar",
        "subcategory": "Craft Brewery",
        "address": "4500 5th Ave S, Montgomery, AL 36108",
        "neighborhood": "West Montgomery",
        "description": "Award-winning craft brewery that put Montgomery on the craft beer map. Taproom featuring rotating taps of their signature ales and lagers. Live music events, food trucks on weekends. Dog-friendly outdoor space.",
        "hours": "Wed-Thu 4pm-10pm, Fri 3pm-11pm, Sat 12pm-11pm, Sun 12pm-8pm",
        "price_range": "$$",
        "points": 150,
        "photo_ref": "ATCDNfUe-MTMFrSBuECu9HYkiELdFHslYbmio4Evi3vQkNPaNXmCZN_RdOzLNq3pGPDkxWGhrr75bXc-YjBjqZwqNY31lI_K7o3nlnKnBUaGwBn-1hUIU_ylqRU7pugWeFOlzoYhU08PWoCxKIJGb5C6KwqFLUfQE1L-v-0gVqzyVsdAVHZkaBNQHJNPb0lWvOuIM9q4xAroseQXYZ542GRQihV3c3oa9eV6rFHqsEQVNjXscS7yva_8FLnzmR9q67kP9aDfB_wO7rE8ZBH3JEQqgHpvkbs4q-oBhMbB1VgSUtAG5SipZUDxGAJl9hrSqckyLgw6NeEjt4_tdW6k2Jk4BgsegrfmYhKutlAZznUZvW5Z9xVyCyz5lLMCbghGdrI-OlfOi_AOeKiTfLM4IGEe46iryMclKR-pOygMBhF-BgDtOEe3fjtwZbb84-R8LKPa0dtCwGyeW__P1vK4gGzT839rADOFsQeposwi4Ao4_Art89zYLeKUh1gZFXY6k7bZpqvwjZXoQ9mMO59yqHV5bcOwAkYDr4osA9H7EfvBvkoU__yeqHcIRZyDVLSqPOWsqdmbEAtF",
        "tags": ["craft beer", "brewery", "live music", "dog-friendly", "outdoor", "casual"],
    },
    {
        "id": "bar_002",
        "name": "Sky Bar Rooftop",
        "category": "Bar",
        "subcategory": "Rooftop Bar",
        "address": "88 Commerce St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Montgomery's premier rooftop bar with breathtaking 360-degree views of the city skyline and Alabama River. Signature cocktails inspired by Alabama heritage. Best spot to watch the sunset over Montgomery.",
        "hours": "Wed-Sun 5pm-midnight",
        "price_range": "$$$",
        "points": 200,
        "photo_ref": "ATCDNfXsR7Mrqb3eL1t8UMyNwFeHMFhjhD7wxIKc99B1dJ2US5Eo65LATZxr1sB6vk4rSG1n9Pp2vh1SgT5yGx-4pSJmOA-DR5mxA5zKITAqgVXg6moJTKksn2Yd_ubCmJ5iBKfLmQ0J1V0YHq79hOC6kNzqOZbjCzVrNtPzsJyNRIBPqy0oz3T39w2sPmfFum-QMWHzzPBaik18Sfm3g1OSVSR9MN38qa90BaNxioEOXsHDukmHAl61QVJPRbPC3im3-8HMxwFM-BIUDXFUHPsSsb5byJyppngqyxVSjHMtE5r_xYp2uJ0",
        "tags": ["rooftop", "cocktails", "views", "upscale", "date night", "sunset"],
    },
    {
        "id": "bar_003",
        "name": "Irish Bred Pub",
        "category": "Bar",
        "subcategory": "Irish Pub",
        "address": "130 Commerce St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Authentic Irish pub experience in downtown Montgomery. 20+ beers on draft, live Celtic music on weekends, and classic pub grub. Known for their St. Patrick's Day celebrations and sports viewing parties.",
        "hours": "Mon-Sun 11am-2am",
        "price_range": "$$",
        "points": 125,
        "photo_ref": "ATCDNfUMVRtW9mFn9iE-g3V7j8jB2feEZhC0bDJzfqf3SpD8oNo9exbyKE5jWdnhA3smWhs-mxIYJnPPeu1ybuOjrtXS_0RM_ylzHWgjEkvqB4NrZkLAyQGUvrgouGYFr57iY3lh75b8W3PWfNOmhB2UR9XwEQaaoMFjlEBogQtpfMd9uGN-xpRLCzkE_bWlDatJjVjJY2GTyl7-olf-Kr9YavNnDPbbvWZppLvLbiPMFe85WF8J0Q1maZXB-0REvJ2ctwPalbFS2fcu1TbZ-FPSyIFk0i0M6BGqJPyjqd7aTelbo9eg",
        "tags": ["irish pub", "sports bar", "draft beer", "live music", "casual", "downtown"],
    },

    # ── ATTRACTIONS ───────────────────────────────────────────────
    {
        "id": "attr_001",
        "name": "Rosa Parks Museum",
        "category": "Attraction",
        "subcategory": "Civil Rights Museum",
        "address": "252 Montgomery St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Powerful museum at the exact site where Rosa Parks was arrested in 1955, sparking the Montgomery Bus Boycott. Features life-size reconstructions, original artifacts, and immersive exhibits about the Civil Rights Movement. A must-visit for all Montgomery visitors.",
        "hours": "Mon-Fri 9am-5pm, Sat 9am-3pm",
        "price_range": "$",
        "points": 300,
        "photo_ref": "ATCDNfXdRUza7cm72_emWRrBsEZ1cZE0SXdF08spkJi30E7mMBTIPpiUkyxDIsB_jAi4ywVvoefqg11ywA_LKWM4YcIEi8UuDk66kv7pMHkFWjCBdg55mt_RZnvYZ1z5Ll-rQSFVR9FvsYdCs9czV9v7O9PFe3Hwhb8_SI2icdvL-bwobI0QzowURFDs2pHFqFrMi3jwfVBB7OyQdC68B-3b3HlyJIAzVC48dh02VMxVUBqWNPpF1Av_zAFB1trpe9JoQm5rrR8mWBIaY8Dc2OW6THY1QjlOTUsDZoWN-aa2FwJ_jXvR7gZVuBmZGRo-BTPVqkqwdeISugDKA8SFn7vLwY9kXcC_mqQ4Y3ByuoJRr0XTZT-lcrq6MK8oT0aTUfweX2FMTyA6rMycbKMc_LTm8H5KRhZAaI_a4s1RsW9_CvUccmo-P0jUNkbHggfg9OHzb0PlSqa-ACYzRNx0DT_-_vGTLvLqIKA-dN4sSfcDnUtzDI0y2i6BHTMQokhScuU_3xLJ9sqnRbsvaKRtoI6rK1IWxsN1eRPtT2mDjOs6S2UEf8TTBNVmTKYMeRsX2LNpVvHcbhVaENA12JeTpSQMeECOolWd3Q",
        "tags": ["civil rights", "history", "museum", "iconic", "educational", "must-visit"],
    },
    {
        "id": "attr_002",
        "name": "Riverwalk Stadium",
        "category": "Attraction",
        "subcategory": "Sports Venue",
        "address": "200 Coosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Home of the Montgomery Biscuits, the beloved Double-A baseball affiliate of the Tampa Bay Rays. One of the most beautiful minor league ballparks in America with stunning views of the Alabama River. Famous for its giant biscuit mascot and family-friendly atmosphere.",
        "hours": "Game days vary — check schedule",
        "price_range": "$",
        "points": 250,
        "photo_ref": "ATCDNfWlaz4NNTzxu6-WBCdoeTo3B9MfsrPOzjj6I7qjLcM5l_U4zwrG6KdaUQZZ5EviWYP5WtZ0NghEpzhm6zQnS_t2BFjjmHVyZjGgDyWJUSXy_6v9Au1wefboQNSaXAYEPTcvh2sjBQnYc9feoo5XLTZwMBvooYs1X8JYeR5TUC-0I47ZJsgP8lGUldI5fK0qmfQXHwSrMNvXX077cJTJbGp0Pwk_VDg7BNxtRF5ZydgcfDUncR_qPHfZon8PQ_c_5kQ17_w_SrWxOjq0YM4LH0QYKR16lIJoqJ0Od6y8VBA8gPO3VR4PyX81sru1_MGcP267uwaPEdBo8mm7RnSTZ9F-8sA4XWgU2ts-DHwFXK4BkkwzOcypwKKe8d31N5qhd4J34_XGsz0DuqewHxqWPoMBHuAAPyHinJeDl841EnuKn0WiPnalt9FrZBo2WGTA_TEyQ-qHbqKTu34nZP1vd6T9ul6eN2MYLOCyefIp74ecKPnQtkN2tFEoFp7hxyG4bUHlk4-WrPjAq_KovO7x7JzS5CiRsI0eDiQ09Nsd7zMgNu3uk4unJfu__2uY69rRS_PuxOjJ",
        "tags": ["baseball", "sports", "family-friendly", "outdoor", "entertainment", "river views"],
    },
    {
        "id": "attr_003",
        "name": "Montgomery Zoo",
        "category": "Attraction",
        "subcategory": "Zoo",
        "address": "2301 Coliseum Pkwy, Montgomery, AL 36110",
        "neighborhood": "North Montgomery",
        "description": "40-acre zoological park home to over 500 animals representing 150+ species from around the world. Features the Mann Wildlife Learning Museum with Alabama wildlife exhibits. Popular Mann Museum and African plains habitat. Great for families and wildlife enthusiasts.",
        "hours": "Daily 9am-5pm",
        "price_range": "$$",
        "points": 250,
        "photo_ref": "ATCDNfUvz5uhMxCUM5g6Xton2nS-xFkk5I8omiJ7_AAldo2CNCIWC21ClMOFmNuok0ETBS7nF7t7pzh6D54FJEpidbBwlK9u22QUfTRO0PvLx4Kq5qfL2vO1aD7ZFIXoRXlOgmxtgmt20LkgG9h7edlqRKe-II88N2RT6C5LtTTBvndFmupdCb6p-BCIzPd3zcwOLoiA2APCy0PAc9tsvclVWZ1tUWFzFU08DY1RXPsS-5XjfgkbzQeW_O2emcmIEvZPg4o0t-8lGN6W1SGnSW8yGxTSFOsy4O3Pdht_Jm47IyrKPdFjDO3q3_o8-bXfl-YElzVTnMDCb5byV4KH1nKPXXMkNUWTVZTO51xsOA14i0PmB-jK1NILtbQ1ARA0wxoDU3MsdJR6mRNY8CNE-7siwoTPxC0Q_SFT_hS6f-iDMfMrrVJ2oEF_0bnw2RrpvSI0E8ajIxLqftNGxUDGUnCBQn7eeYhFQMLonMDuKGjxJc3v7Nx2LVD18ymb3kJZ0Jz7gy_aFD1k4H5nwUpveJ4qyln7bZ9EwfSr1cPcPm-enycs42C79y7Iuc_LWr_xfdJ8FY2ytKBuy016IA",
        "tags": ["zoo", "animals", "family-friendly", "outdoor", "educational", "kids"],
    },
    {
        "id": "attr_004",
        "name": "Alabama State Capitol",
        "category": "Attraction",
        "subcategory": "Historic Landmark",
        "address": "600 Dexter Ave, Montgomery, AL 36130",
        "neighborhood": "Downtown",
        "description": "The historic Alabama State Capitol where Jefferson Davis was inaugurated as President of the Confederacy in 1861. Also the endpoint of the famous Selma to Montgomery marches in 1965. Free tours available. One of the most historically significant buildings in American history.",
        "hours": "Mon-Fri 9am-5pm",
        "price_range": "Free",
        "points": 200,
        "photo_ref": "ATCDNfX4JAQ0-IM5gnPYBQe6S9mAmYzY4NKjn9xw2qVUXzw4UjqF671jtozRFbrtmzMRFuafBO_qZjf2aMjXB4PF1QjpkXul73YAJwI41IMSc_2EP8EQP7AmorU7WzRAPTpccG4lCyAWz8EGcYDrPGy18ciGfbEtDpJs00ZjJTg6PfL3Cw5lJDh5zoWccxN1QbkcyR3oOpZha5e88GmmWiY9BKt2T1VSXKNcxs-ZUBQr79vw7DZQa7HIBQIFlLo97GKJMKbtSOAFnOaDXnoEc4omk329oLZHCjY6nYhNkVHt6n8e8ye7C0SKigEz3jUWWNOGLpJqt8q3faCb0qBd916D60P85OwGQwtDtYRF7UASuufGgRNFvEneWHJi9znfXKDCFRQAyVh-ittgA_omj9C30ZwC83vRUR8SZyMHNYMLVFKir5VE2uXIsL86NTlR64kwTFGqSGSwXF6j266QxUKSucVP8ii9Y3Pl1D7nnWal9VpMZ8TLLb97G-H7yKpuAH7Mmz6CfumPS9_nFJI1le-DK3EwfKilfuWpLl_o0iYyNlM8seOE7bUIO--mk198IUEkwNywttK3",
        "tags": ["historic", "civil rights", "architecture", "free", "landmark", "history"],
    },
    {
        "id": "attr_005",
        "name": "National Memorial for Peace and Justice",
        "category": "Attraction",
        "subcategory": "Memorial & Museum",
        "address": "417 Caroline St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "The nation's first memorial dedicated to the legacy of enslaved Black Americans and victims of racial terror lynching. Created by the Equal Justice Initiative. Profoundly moving outdoor installation with 800 suspended steel monuments. One of the most important cultural sites in America.",
        "hours": "Wed-Mon 9am-5pm",
        "price_range": "$",
        "points": 350,
        "photo_ref": "ATCDNfVqLMENwtCE9yxW0mm-65Jbvyq31hriAGdYC-Qf9mia_MFhLWp7dFexvgpEhHYU5QgG0QzaI71B2ZWq1OFMmdKKyw-wnhdqfH-NXC2tS0PfCVAnNx-UOZqNSb3Md5nbk6TfOns88GQ88ueeaPfmR5V-NKA3lPq2sCipSuPN_U1C-blTqHKFR92NeS534i-z6XLrVBKOIkIlpw-4QdZJZQMathUs05mkVHqQw8AGsnHYEC_YKNvy4q-6DY-Gdjkxyz48Bi_vHfL7LVXAaV-r-gqSAkLmUvJI03mW41a_q911t4NSQkp_NnUjlB2Ank2szT34z9zrU6CA9WrXU8ELTGUE2v49pk6rhyAW8-I6_Tu9CTUfcO3qhqkwF0trQ8QJj5UYg1FzzJ7jLAxGyec8pOnGkxbNimN4qOJqICaXj7nyaPqf5dzphhjgWCzPXvReARP8idzvMKuLWWPZyICFmXhyo7D8vnGwt3TpfY7n9M02OnBO8Hq0uHmpcdtEFcwSrKW9zgvDJ69OSw3vKormTWcIo--SFXMpJGtfQ5jj64kI7jGOvP73soON6wnlvJ55eER5lWn2",
        "tags": ["memorial", "civil rights", "history", "must-visit", "powerful", "educational"],
    },
    {
        "id": "attr_006",
        "name": "Legacy Museum",
        "category": "Attraction",
        "subcategory": "Museum",
        "address": "115 Coosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Groundbreaking museum by the Equal Justice Initiative exploring the history of racial inequality in America from slavery to mass incarceration. Built on the site of a former warehouse where enslaved people were held. Features immersive technology and powerful narratives.",
        "hours": "Wed-Mon 9am-5pm",
        "price_range": "$$",
        "points": 300,
        "photo_ref": "ATCDNfVtEFJf5_vRICukynewF_SemGCGQ_-0ZDPYHEjOW_rwJ91LbGCA3mW98tBbevmsX4HZf7ONyhn7twFfEjRx4-_HQNg0C-2MAitWKeljd04aQdutiYTNx2W1g-2Oi4wgji2XjLsoQdp4iEP1V9PIFwD2BuNIIuZnYPpwZOtGTMrftEU44PGxPQ0wiLoqPDUNJcFQljfJKVuseqpSiDNd6GFvvCPcN9ejpW5kbThlthl9ulSPnIQKa0VHMIzJdJ0p5IH11OaBoP_bByjUGGccY983xCRwoW7gjoJlt4PXUBqwVDehq7k",
        "tags": ["museum", "civil rights", "history", "educational", "powerful", "must-visit"],
    },
    {
        "id": "attr_007",
        "name": "Dexter Avenue King Memorial Baptist Church",
        "category": "Attraction",
        "subcategory": "Historic Church",
        "address": "454 Dexter Ave, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Where Dr. Martin Luther King Jr. served as pastor from 1954-1960 and organized the Montgomery Bus Boycott. A National Historic Landmark and one of the most important sites of the Civil Rights Movement. Guided tours available of the historic church and Dr. King's basement office.",
        "hours": "Mon-Fri 10am-4pm",
        "price_range": "$",
        "points": 300,
        "photo_ref": "ATCDNfXnlvF6WolZKQwx21EmU9w2Ql4zY1xBuvMfIjpj2_yBlxNK72FZovpNSYOdDr-tsQw1d-r_hJzD_bqyxtZkXiqLJWczSAXhhErjbLox5iK49MZ1e78pvpjE-D9wWg61jRXOm-wAlyHjKJxVAJ_yzbuPLzU9E85uM0Q_bXq6ziS-VuLdwByhau0TVe_AtYMK4ruzfEr1ofVRXkNVOlTve4jki4SHY76piyeRMqyglOhoHGI6-uemC4vzoCwKRPEe8fHn2rH7w0C-f6FiR_4A7IZOQv7BtFmffbm6DXQVE9etSWx3OWrb_UNahf_WzRhsdKlljAt-cyDnzggU8WQgtTIyWxok648_0pwo9iw_OH8dm6wM7llq_4LjnFieAjYzQYAcokHjp4YJZ_Qlb0hzAICT_NyMUAAFQ7aacRvTvuzA3WC3i8p7k0fJPhTXe9UbRKD1B2jNbkkbnf7sjG-9fJwsv8C07pBPS4vjHMWcDNM_ujYBKBvVMayz2w7e89dhGQwiSwH_sFnbcklIECzshEXbtuwTwDT1sUP1h582L3seLOo85DbuycED0-iybuXluVhWqvZlAuukFg",
        "tags": ["civil rights", "MLK", "historic", "church", "landmark", "tours"],
    },
    {
        "id": "attr_008",
        "name": "Alabama Shakespeare Festival",
        "category": "Attraction",
        "subcategory": "Theater & Arts",
        "address": "1 Festival Dr, Montgomery, AL 36117",
        "neighborhood": "East Montgomery",
        "description": "One of the largest Shakespeare festivals in the world and the official state theatre of Alabama. Two beautiful theaters set in the stunning 250-acre Blount Cultural Park. Year-round performances ranging from Shakespeare classics to contemporary works and musicals.",
        "hours": "Varies by performance",
        "price_range": "$$$",
        "points": 250,
        "photo_ref": "ATCDNfX1A1vgmxrCc8OC7US_WkVHsieym8lX16zJy-7loq2C3g8H1ntWY-mD0x_ljCMzvdvR99fhVrAI3JBRT2feYBNdiYbLwNDwlPsool_NpKhrfBgIst2XM-whe78KWpIIs7wS0GubjVOsjZoWbiiJBK2WBXfnUPvuI2ZfT_j_4h8_Sx6PwFW3rZtw-SiCY3ivBIDkbQ2lSJGV5zKckm1FV7AMjekOLnGlnY8s3QgG6646a--NZuHPuwCu5mT3UKmoacdLJetucWEuxwKlKnTcrZJWvcVcjbXCvf6YLfziO5QwRMZu8ybqnu9pHq4bkxsd6LmIrZKosbxsrlsqYxmfSxnwYjcVAjBGZUD6YyF8vwnrw-vSADti2NqA5Aj89AlF6aFBJrPStMsll_0ZY98ivaUWv2Sxi2dtyD5N5JFtLdwUCsTHDqucmyfAJkgFRP5Np_zEjuV0YcTcffGEG9NBdNd0k_Tu5K2-7WbIRNGSBVMxGz7_TDTINOo74Dd0byN_w96suWBYsoUMZf0487XoI66jrBUZMwOxMWdXpwOh9l4bdTxvcaUGY3r6MtCowlCqx8f4cA",
        "tags": ["theater", "arts", "shakespeare", "culture", "entertainment", "upscale"],
    },

    # ── HOTELS ────────────────────────────────────────────────────
    {
        "id": "hotel_001",
        "name": "Renaissance Montgomery Hotel",
        "category": "Hotel",
        "subcategory": "Luxury Hotel",
        "address": "201 Tallapoosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Montgomery's premier luxury hotel connected to the Convention Center and RSA Activity Center. Elegant rooms with stunning city views, rooftop pool, and upscale dining. Steps from all major downtown attractions and the Alabama River.",
        "hours": "24/7",
        "price_range": "$$$",
        "points": 200,
        "photo_ref": "ATCDNfUOhyG-MCvDCtMzzvXucTblTj056g2-CC_PJrZPMnx3JVix6_dpiCZFegxh_shtGcuxDSexmPZe0m3T9VDQQz4aTZw6hbfxAJ9mRnDW1NJzaSNgnnKgAwTKLiccXaCeMreHRcifGRzbZLyY6iHvV51bYVEfa69BN2_a_ttFChVpgFumXgOSagkVGAjj9qu29-c8R_wOZeUEcQ0EEJVmjCYtrQlJDdzPMAaDGaKSxUBceRSuuDFx05S8SSfSPdaen7blgNFSQZXy4EtcRuvIr7sQqgMEhSyLQz_pDanj-8R2AjtL4_I",
        "tags": ["luxury", "hotel", "downtown", "rooftop pool", "convention", "business"],
    },
    {
        "id": "hotel_002",
        "name": "Marriott Autograph Collection — The Lattice",
        "category": "Hotel",
        "subcategory": "Boutique Hotel",
        "address": "100 Commerce St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Boutique luxury hotel in a beautifully restored historic downtown building. Features locally-inspired design, craft cocktail bar, and farm-to-table restaurant. Walking distance to all major civil rights landmarks and riverfront attractions.",
        "hours": "24/7",
        "price_range": "$$$",
        "points": 200,
        "photo_ref": "ATCDNfWlyQzx9DEnpHOzBgMRQl69fcVruHqO7Hp4LYxhM8qKH0u1Yy40isiPp5e-1mliZgaX-DacdilJp8FiJlat1I1IHzXdyoluTsIyzJr58a7mHa1GUBbuQLqfCx-qGr_KRRpz8G82OuoLe1ItC8drgDr4yxCvz1TgU-GKvEjiGuJeXGNky59vAkJE4S9GSez2psHa1joykPUTnTLcpGAUV5dna5ShF6YSeePuZG7uajSFZ8QGwxv2YnGYGCvmuUOebZaWMQWzqwJpZGAzRCtY61OsN7ZbMpwxtRQSOVzya3_UEVs1MOs",
        "tags": ["boutique", "historic", "luxury", "hotel", "downtown", "walkable"],
    },
]

def get_all_places():
    return MONTGOMERY_PLACES

def get_places_by_category(category: str):
    return [p for p in MONTGOMERY_PLACES if p["category"].lower() == category.lower()]

def get_place_by_id(place_id: str):
    return next((p for p in MONTGOMERY_PLACES if p["id"] == place_id), None)

def get_places_as_documents():
    """Format places as text documents for ChromaDB ingestion."""
    docs = []
    for place in MONTGOMERY_PLACES:
        doc = f"""
Name: {place['name']}
Category: {place['category']} — {place['subcategory']}
Address: {place['address']}
Neighborhood: {place['neighborhood']}
Description: {place['description']}
Hours: {place['hours']}
Price Range: {place['price_range']}
Ventur Points: {place['points']} pts
Tags: {', '.join(place['tags'])}
        """.strip()
        docs.append({"id": place["id"], "text": doc, "metadata": place})
    return docs

if __name__ == "__main__":
    docs = get_places_as_documents()
    print(f"✅ {len(docs)} places ready to load into ChromaDB!")
    for doc in docs:
        print(f"  - [{doc['metadata']['category']}] {doc['metadata']['name']}")
