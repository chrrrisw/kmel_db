STRING_ENCODING = "utf_16_le"

OFFSETS_OFFSET = 0x40

# The following is the list of offsets in the offset table - DO NOT CHANGE
# TO INCLUDE ANYTHING ELSE
(
    main_index_offset,
    title_offset,
    shortdir_offset,
    shortfile_offset,

    longdir_offset,
    longfile_offset,
    alpha_title_order_offset,
    genre_index_offset,

    genre_name_offset,
    genre_title_offset,
    genre_title_order_offset,
    performer_index_offset,

    performer_name_offset,
    performer_title_offset,
    performer_title_order_offset,
    album_index_offset,

    album_name_offset,
    album_title_offset,
    album_title_order_offset,
    u20_offset,

    playlist_index_offset,
    playlist_name_offset,
    playlist_title_offset,
    u24_offset,

    u25_offset,
    u26_offset,
    u27_offset,
    sub_index_offset,

    u29_offset,
    u30_offset,
    u31_offset,
    u32_offset,
    end_offsets
) = list(range(33))

(
    sub_0_genre_performers,
    sub_1_genre_performer_albums,
    sub_2_genre_performer_album_titles,
    sub_3_genre_ordered_titles,
    sub_4_genre_albums,
    sub_5_genre_album_titles,
    sub_6_genre_titles,
    sub_7_performer_albums,
    sub_8_performer_album_titles,
    sub_9_performer_titles,
    sub_10_genre_performers,
    sub_11_genre_performer_titles,
    sub_12_genre_ordered_titles,
    end_subindex_offsets
) = list(range(14))
