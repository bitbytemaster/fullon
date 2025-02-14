#!/usr/bin/env python3

import random

from TestHarness import Cluster, TestHelper, Utils, WalletMgr

###############################################################
# terminate-scenarios-test
#
# Tests terminate scenarios for gaxnod.  Uses "-c" flag to indicate "replay" (--replay-blockchain), "resync"
# (--delete-all-blocks), "hardReplay"(--hard-replay-blockchain), and "none" to indicate what kind of restart flag should
# be used. This is one of the only test that actually verify that gaxnod terminates with a good exit status.
#
###############################################################


Print=Utils.Print
errorExit=Utils.errorExit

args=TestHelper.parse_args({"-d","-s","-c","--kill-sig","--keep-logs"
                            ,"--dump-error-details","-v","--leave-running","--clean-run"
                            ,"--terminate-at-block","--unshared"})
pnodes=1
topo=args.s
delay=args.d
chainSyncStrategyStr=args.c
debug=args.v
total_nodes = pnodes
killSignal=args.kill_sig
killEosInstances= not args.leave_running
dumpErrorDetails=args.dump_error_details
keepLogs=args.keep_logs
killAll=args.clean_run
terminate=args.terminate_at_block

seed=1
Utils.Debug=debug
testSuccessful=False

random.seed(seed) # Use a fixed seed for repeatability.
cluster=Cluster(walletd=True,unshared=args.unshared)
walletMgr=WalletMgr(True)

try:
    TestHelper.printSystemInfo("BEGIN")
    cluster.setWalletMgr(walletMgr)

    cluster.setChainStrategy(chainSyncStrategyStr)
    cluster.setWalletMgr(walletMgr)

    cluster.killall(allInstances=killAll)
    cluster.cleanup()
    walletMgr.killall(allInstances=killAll)
    walletMgr.cleanup()

    Print ("producing nodes: %d, topology: %s, delay between nodes launch(seconds): %d, chain sync strategy: %s" % (
    pnodes, topo, delay, chainSyncStrategyStr))

    Print("Stand up cluster")
    if cluster.launch(pnodes=pnodes, totalNodes=total_nodes, topo=topo, delay=delay) is False:
        errorExit("Failed to stand up eos cluster.")

    Print ("Wait for Cluster stabilization")
    # wait for cluster to start producing blocks
    if not cluster.waitOnClusterBlockNumSync(3):
        errorExit("Cluster never stabilized")

    Print("Kill cluster node instance.")
    if cluster.killSomeEosInstances(1, killSignal) is False:
        errorExit("Failed to kill Eos instances")
    assert not cluster.getNode(0).verifyAlive()
    Print("gaxnod instances killed.")

    Print ("Relaunch dead cluster node instance.")
    nodeArg = "--terminate-at-block %d" % terminate if terminate > 0 else ""
    if nodeArg != "":
        if chainSyncStrategyStr == "hardReplay":
            nodeArg += " --truncate-at-block %d" % terminate
    if cluster.relaunchEosInstances(cachePopen=True, nodeArgs=nodeArg, waitForTerm=(terminate > 0)) is False:
        errorExit("Failed to relaunch Eos instance")
    Print("gaxnod instance relaunched.")

    testSuccessful=True
finally:
    TestHelper.shutdown(cluster, walletMgr, testSuccessful=testSuccessful, killEosInstances=killEosInstances, killWallet=killEosInstances, keepLogs=keepLogs, cleanRun=killAll, dumpErrorDetails=dumpErrorDetails)

exitCode = 0 if testSuccessful else 1
exit(exitCode)