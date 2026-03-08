# Immich Database Schema

## `activity`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `albumId` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `assetId` | `UUID` | ✅ |
| `comment` | `TEXT` | ✅ |
| `isLiked` | `BOOLEAN` | ❌ |
| `updateId` | `UUID` | ❌ |

## `album`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `albumName` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `albumThumbnailAssetId` | `UUID` | ✅ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `description` | `TEXT` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `isActivityEnabled` | `BOOLEAN` | ❌ |
| `order` | `VARCHAR` | ❌ |
| `updateId` | `UUID` | ❌ |

## `album_asset`

| Column | Type | Nullable |
|--------|------|----------|
| `albumId` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `updateId` | `UUID` | ❌ |

## `album_asset_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `albumId` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `album_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `albumId` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `album_user`

| Column | Type | Nullable |
|--------|------|----------|
| `albumId` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `role` | `VARCHAR` | ❌ |
| `updateId` | `UUID` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `createId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |

## `album_user_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `albumId` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `api_key`

| Column | Type | Nullable |
|--------|------|----------|
| `name` | `VARCHAR` | ❌ |
| `key` | `VARCHAR` | ❌ |
| `userId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `id` | `UUID` | ❌ |
| `permissions` | `ARRAY` | ❌ |
| `updateId` | `UUID` | ❌ |

## `asset`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `deviceAssetId` | `VARCHAR` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `deviceId` | `VARCHAR` | ❌ |
| `type` | `VARCHAR` | ❌ |
| `originalPath` | `VARCHAR` | ❌ |
| `fileCreatedAt` | `TIMESTAMP` | ❌ |
| `fileModifiedAt` | `TIMESTAMP` | ❌ |
| `isFavorite` | `BOOLEAN` | ❌ |
| `duration` | `VARCHAR` | ✅ |
| `encodedVideoPath` | `VARCHAR` | ✅ |
| `checksum` | `BYTEA` | ❌ |
| `livePhotoVideoId` | `UUID` | ✅ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `originalFileName` | `VARCHAR` | ❌ |
| `thumbhash` | `BYTEA` | ✅ |
| `isOffline` | `BOOLEAN` | ❌ |
| `libraryId` | `UUID` | ✅ |
| `isExternal` | `BOOLEAN` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `localDateTime` | `TIMESTAMP` | ❌ |
| `stackId` | `UUID` | ✅ |
| `duplicateId` | `UUID` | ✅ |
| `status` | `VARCHAR(7)` | ❌ |
| `updateId` | `UUID` | ❌ |
| `visibility` | `VARCHAR(8)` | ❌ |
| `width` | `INTEGER` | ✅ |
| `height` | `INTEGER` | ✅ |
| `isEdited` | `BOOLEAN` | ❌ |

## `asset_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `asset_edit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `action` | `VARCHAR` | ❌ |
| `parameters` | `JSONB` | ❌ |
| `sequence` | `INTEGER` | ❌ |

## `asset_exif`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `make` | `VARCHAR` | ✅ |
| `model` | `VARCHAR` | ✅ |
| `exifImageWidth` | `INTEGER` | ✅ |
| `exifImageHeight` | `INTEGER` | ✅ |
| `fileSizeInByte` | `BIGINT` | ✅ |
| `orientation` | `VARCHAR` | ✅ |
| `dateTimeOriginal` | `TIMESTAMP` | ✅ |
| `modifyDate` | `TIMESTAMP` | ✅ |
| `lensModel` | `VARCHAR` | ✅ |
| `fNumber` | `DOUBLE PRECISION` | ✅ |
| `focalLength` | `DOUBLE PRECISION` | ✅ |
| `iso` | `INTEGER` | ✅ |
| `latitude` | `DOUBLE PRECISION` | ✅ |
| `longitude` | `DOUBLE PRECISION` | ✅ |
| `city` | `VARCHAR` | ✅ |
| `state` | `VARCHAR` | ✅ |
| `country` | `VARCHAR` | ✅ |
| `description` | `TEXT` | ❌ |
| `fps` | `DOUBLE PRECISION` | ✅ |
| `exposureTime` | `VARCHAR` | ✅ |
| `livePhotoCID` | `VARCHAR` | ✅ |
| `timeZone` | `VARCHAR` | ✅ |
| `projectionType` | `VARCHAR` | ✅ |
| `profileDescription` | `VARCHAR` | ✅ |
| `colorspace` | `VARCHAR` | ✅ |
| `bitsPerSample` | `INTEGER` | ✅ |
| `autoStackId` | `VARCHAR` | ✅ |
| `rating` | `INTEGER` | ✅ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `updateId` | `UUID` | ❌ |
| `lockedProperties` | `ARRAY` | ✅ |
| `tags` | `ARRAY` | ✅ |

## `asset_face`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `personId` | `UUID` | ✅ |
| `imageWidth` | `INTEGER` | ❌ |
| `imageHeight` | `INTEGER` | ❌ |
| `boundingBoxX1` | `INTEGER` | ❌ |
| `boundingBoxY1` | `INTEGER` | ❌ |
| `boundingBoxX2` | `INTEGER` | ❌ |
| `boundingBoxY2` | `INTEGER` | ❌ |
| `id` | `UUID` | ❌ |
| `sourceType` | `VARCHAR(16)` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `updateId` | `UUID` | ❌ |
| `isVisible` | `BOOLEAN` | ❌ |

## `asset_face_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `assetFaceId` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `asset_file`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `type` | `VARCHAR` | ❌ |
| `path` | `VARCHAR` | ❌ |
| `updateId` | `UUID` | ❌ |
| `isEdited` | `BOOLEAN` | ❌ |
| `isProgressive` | `BOOLEAN` | ❌ |

## `asset_job_status`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `facesRecognizedAt` | `TIMESTAMP` | ✅ |
| `metadataExtractedAt` | `TIMESTAMP` | ✅ |
| `duplicatesDetectedAt` | `TIMESTAMP` | ✅ |
| `ocrAt` | `TIMESTAMP` | ✅ |

## `asset_metadata`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `key` | `VARCHAR` | ❌ |
| `value` | `JSONB` | ❌ |
| `updateId` | `UUID` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |

## `asset_metadata_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `key` | `VARCHAR` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `asset_ocr`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `x1` | `REAL` | ❌ |
| `y1` | `REAL` | ❌ |
| `x2` | `REAL` | ❌ |
| `y2` | `REAL` | ❌ |
| `x3` | `REAL` | ❌ |
| `y3` | `REAL` | ❌ |
| `x4` | `REAL` | ❌ |
| `y4` | `REAL` | ❌ |
| `boxScore` | `REAL` | ❌ |
| `textScore` | `REAL` | ❌ |
| `text` | `TEXT` | ❌ |
| `isVisible` | `BOOLEAN` | ❌ |

## `audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `INTEGER` | ❌ |
| `entityType` | `VARCHAR` | ❌ |
| `entityId` | `UUID` | ❌ |
| `action` | `VARCHAR` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |

## `face_search`

| Column | Type | Nullable |
|--------|------|----------|
| `faceId` | `UUID` | ❌ |
| `embedding` | `NULL` | ❌ |

## `geodata_places`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `INTEGER` | ❌ |
| `name` | `VARCHAR(200)` | ❌ |
| `longitude` | `DOUBLE PRECISION` | ❌ |
| `latitude` | `DOUBLE PRECISION` | ❌ |
| `countryCode` | `CHAR(2)` | ❌ |
| `admin1Code` | `VARCHAR(20)` | ✅ |
| `admin2Code` | `VARCHAR(80)` | ✅ |
| `modificationDate` | `DATE` | ❌ |
| `admin1Name` | `VARCHAR` | ✅ |
| `admin2Name` | `VARCHAR` | ✅ |
| `alternateNames` | `VARCHAR` | ✅ |

## `kysely_migrations`

| Column | Type | Nullable |
|--------|------|----------|
| `name` | `VARCHAR(255)` | ❌ |
| `timestamp` | `VARCHAR(255)` | ❌ |

## `kysely_migrations_lock`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `VARCHAR(255)` | ❌ |
| `is_locked` | `INTEGER` | ❌ |

## `library`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `name` | `VARCHAR` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `importPaths` | `ARRAY` | ❌ |
| `exclusionPatterns` | `ARRAY` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `refreshedAt` | `TIMESTAMP` | ✅ |
| `updateId` | `UUID` | ❌ |

## `memory`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `ownerId` | `UUID` | ❌ |
| `type` | `VARCHAR` | ❌ |
| `data` | `JSONB` | ❌ |
| `isSaved` | `BOOLEAN` | ❌ |
| `memoryAt` | `TIMESTAMP` | ❌ |
| `seenAt` | `TIMESTAMP` | ✅ |
| `showAt` | `TIMESTAMP` | ✅ |
| `hideAt` | `TIMESTAMP` | ✅ |
| `updateId` | `UUID` | ❌ |

## `memory_asset`

| Column | Type | Nullable |
|--------|------|----------|
| `memoriesId` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `updateId` | `UUID` | ❌ |

## `memory_asset_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `memoryId` | `UUID` | ❌ |
| `assetId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `memory_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `memoryId` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `migration_overrides`

| Column | Type | Nullable |
|--------|------|----------|
| `name` | `VARCHAR` | ❌ |
| `value` | `JSONB` | ❌ |

## `move_history`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `entityId` | `UUID` | ❌ |
| `pathType` | `VARCHAR` | ❌ |
| `oldPath` | `VARCHAR` | ❌ |
| `newPath` | `VARCHAR` | ❌ |

## `naturalearth_countries`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `INTEGER` | ❌ |
| `admin` | `VARCHAR(50)` | ❌ |
| `admin_a3` | `VARCHAR(3)` | ❌ |
| `type` | `VARCHAR(50)` | ❌ |
| `coordinates` | `NULL` | ❌ |

## `notification`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `updateId` | `UUID` | ❌ |
| `userId` | `UUID` | ✅ |
| `level` | `VARCHAR` | ❌ |
| `type` | `VARCHAR` | ❌ |
| `data` | `JSONB` | ✅ |
| `title` | `VARCHAR` | ❌ |
| `description` | `TEXT` | ✅ |
| `readAt` | `TIMESTAMP` | ✅ |

## `ocr_search`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `text` | `TEXT` | ❌ |

## `partner`

| Column | Type | Nullable |
|--------|------|----------|
| `sharedById` | `UUID` | ❌ |
| `sharedWithId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `inTimeline` | `BOOLEAN` | ❌ |
| `updateId` | `UUID` | ❌ |
| `createId` | `UUID` | ❌ |

## `partner_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `sharedById` | `UUID` | ❌ |
| `sharedWithId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `person`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `name` | `VARCHAR` | ❌ |
| `thumbnailPath` | `VARCHAR` | ❌ |
| `isHidden` | `BOOLEAN` | ❌ |
| `birthDate` | `DATE` | ✅ |
| `faceAssetId` | `UUID` | ✅ |
| `isFavorite` | `BOOLEAN` | ❌ |
| `color` | `VARCHAR` | ✅ |
| `updateId` | `UUID` | ❌ |

## `person_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `personId` | `UUID` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `plugin`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `name` | `VARCHAR` | ❌ |
| `title` | `VARCHAR` | ❌ |
| `description` | `VARCHAR` | ❌ |
| `author` | `VARCHAR` | ❌ |
| `version` | `VARCHAR` | ❌ |
| `wasmPath` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |

## `plugin_action`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `pluginId` | `UUID` | ❌ |
| `methodName` | `VARCHAR` | ❌ |
| `title` | `VARCHAR` | ❌ |
| `description` | `VARCHAR` | ❌ |
| `supportedContexts` | `ARRAY` | ❌ |
| `schema` | `JSONB` | ✅ |

## `plugin_filter`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `pluginId` | `UUID` | ❌ |
| `methodName` | `VARCHAR` | ❌ |
| `title` | `VARCHAR` | ❌ |
| `description` | `VARCHAR` | ❌ |
| `supportedContexts` | `ARRAY` | ❌ |
| `schema` | `JSONB` | ✅ |

## `session`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `token` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `userId` | `UUID` | ❌ |
| `deviceType` | `VARCHAR` | ❌ |
| `deviceOS` | `VARCHAR` | ❌ |
| `updateId` | `UUID` | ❌ |
| `pinExpiresAt` | `TIMESTAMP` | ✅ |
| `expiresAt` | `TIMESTAMP` | ✅ |
| `parentId` | `UUID` | ✅ |
| `isPendingSyncReset` | `BOOLEAN` | ❌ |
| `appVersion` | `VARCHAR` | ✅ |

## `session_sync_checkpoint`

| Column | Type | Nullable |
|--------|------|----------|
| `sessionId` | `UUID` | ❌ |
| `type` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `ack` | `VARCHAR` | ❌ |
| `updateId` | `UUID` | ❌ |

## `shared_link`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `description` | `VARCHAR` | ✅ |
| `userId` | `UUID` | ❌ |
| `key` | `BYTEA` | ❌ |
| `type` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `expiresAt` | `TIMESTAMP` | ✅ |
| `allowUpload` | `BOOLEAN` | ❌ |
| `albumId` | `UUID` | ✅ |
| `allowDownload` | `BOOLEAN` | ❌ |
| `showExif` | `BOOLEAN` | ❌ |
| `password` | `VARCHAR` | ✅ |
| `slug` | `VARCHAR` | ✅ |

## `shared_link_asset`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `sharedLinkId` | `UUID` | ❌ |

## `smart_search`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `embedding` | `NULL` | ❌ |

## `stack`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `primaryAssetId` | `UUID` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `updateId` | `UUID` | ❌ |

## `stack_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `stackId` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `system_metadata`

| Column | Type | Nullable |
|--------|------|----------|
| `key` | `VARCHAR` | ❌ |
| `value` | `JSONB` | ❌ |

## `tag`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `value` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `color` | `VARCHAR` | ✅ |
| `parentId` | `UUID` | ✅ |
| `updateId` | `UUID` | ❌ |

## `tag_asset`

| Column | Type | Nullable |
|--------|------|----------|
| `assetId` | `UUID` | ❌ |
| `tagId` | `UUID` | ❌ |

## `tag_closure`

| Column | Type | Nullable |
|--------|------|----------|
| `id_ancestor` | `UUID` | ❌ |
| `id_descendant` | `UUID` | ❌ |

## `user`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `email` | `VARCHAR` | ❌ |
| `password` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `profileImagePath` | `VARCHAR` | ❌ |
| `isAdmin` | `BOOLEAN` | ❌ |
| `shouldChangePassword` | `BOOLEAN` | ❌ |
| `deletedAt` | `TIMESTAMP` | ✅ |
| `oauthId` | `VARCHAR` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |
| `storageLabel` | `VARCHAR` | ✅ |
| `name` | `VARCHAR` | ❌ |
| `quotaSizeInBytes` | `BIGINT` | ✅ |
| `quotaUsageInBytes` | `BIGINT` | ❌ |
| `status` | `VARCHAR` | ❌ |
| `profileChangedAt` | `TIMESTAMP` | ❌ |
| `updateId` | `UUID` | ❌ |
| `avatarColor` | `VARCHAR` | ✅ |
| `pinCode` | `VARCHAR` | ✅ |

## `user_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `userId` | `UUID` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |
| `id` | `UUID` | ❌ |

## `user_metadata`

| Column | Type | Nullable |
|--------|------|----------|
| `userId` | `UUID` | ❌ |
| `key` | `VARCHAR` | ❌ |
| `value` | `JSONB` | ❌ |
| `updateId` | `UUID` | ❌ |
| `updatedAt` | `TIMESTAMP` | ❌ |

## `user_metadata_audit`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `userId` | `UUID` | ❌ |
| `key` | `VARCHAR` | ❌ |
| `deletedAt` | `TIMESTAMP` | ❌ |

## `version_history`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `version` | `VARCHAR` | ❌ |

## `workflow`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `ownerId` | `UUID` | ❌ |
| `triggerType` | `VARCHAR` | ❌ |
| `name` | `VARCHAR` | ✅ |
| `description` | `VARCHAR` | ❌ |
| `createdAt` | `TIMESTAMP` | ❌ |
| `enabled` | `BOOLEAN` | ❌ |

## `workflow_action`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `workflowId` | `UUID` | ❌ |
| `pluginActionId` | `UUID` | ❌ |
| `actionConfig` | `JSONB` | ✅ |
| `order` | `INTEGER` | ❌ |

## `workflow_filter`

| Column | Type | Nullable |
|--------|------|----------|
| `id` | `UUID` | ❌ |
| `workflowId` | `UUID` | ❌ |
| `pluginFilterId` | `UUID` | ❌ |
| `filterConfig` | `JSONB` | ✅ |
| `order` | `INTEGER` | ❌ |
