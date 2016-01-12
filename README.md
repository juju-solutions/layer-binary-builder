
## Overview

This charm is used to build the binaries of Gobblin and upload them to S3.
Goblin is a universal data ingestion framework.
[Gobblin wiki](https://github.com/linkedin/gobblin/wiki) 

## Usage
Upon deployment the charm installs the dependencies needed to build and upload the
Gobblin binaries:

    juju deploy gobblin-binary-builder gbuilder


## Testing the deployment

Two actions are available, one for building the binary and one for uploading to S3.

### Building Action
Trigger the build action like this:

    juju action do gbuilder/0 build

The action options available are:

    release: The release version. This string is part of the Gobblin source release tag
    hadoop-version: The Hadoop version we should build Gobblin against
    
During build, the status message of the charm should change from 'Ready' to 'Checking out source',
'Building binary', 'Finishing packaging' and become 'Ready' again.

Fetching the result of the action yields the produced binary and the sha256 digest, eg.

    juju action fetch 9889f266-6634-4e78-85e0-e6f8c3e47522

Returns:

    results:
      binary: /tmp/workspace/gobblin-dist-0.6.0_hadoop-2.7.1-9401863.tar.gz
      sha256sum: 94018632b4b6e5eb9cfeea85b76f0a38d96fbf0ded0748b824a5bb05f21da57e
    status: completed

At this point you can fetch the binary using juju scp facilities:
    
    juju scp gbuilder/0:/tmp/workspace/gobblin-dist-0.6.0_hadoop-2.7.1-9401863.tar.gz .

    
### Uploading a binary
Triggering the uploading action is done like this:

    juju action do gbuilder/0 awsupload "s3-access-key=<your key> s3-secret-key=<your secret key> bucket=<the bucket name>"

In addition to the above three parameters (s3-access-key, s3-secret-key and bucket)
the user has also the option of specifying the region/AWS endpoint via the optional 'aws-endpoint' parameter.

As soon as the uploading action is triggered, the status message of the charm should change to 'Uploading binary'
and will become 'Ready' when the uploading finishes.


## Contact Information

- <bigdata@lists.ubuntu.com>


## Help

- [Juju mailing list](https://lists.ubuntu.com/mailman/listinfo/juju)
- [Juju community](https://jujucharms.com/community)
