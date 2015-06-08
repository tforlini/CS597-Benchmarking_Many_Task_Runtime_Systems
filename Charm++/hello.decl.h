#ifndef _DECL_hello_H_
#define _DECL_hello_H_
#include "charm++.h"
#include "envelope.h"
#include <memory>
#include "sdag.h"
/* DECLS: array Hello: ArrayElement{
Hello(void);
void sayHi(int impl_noname_0);
void sleep(int impl_noname_1);
Hello(CkMigrateMessage* impl_msg);
};
 */
 class Hello;
 class CkIndex_Hello;
 class CProxy_Hello;
 class CProxyElement_Hello;
 class CProxySection_Hello;
/* --------------- index object ------------------ */
class CkIndex_Hello:public CkIndex_ArrayElement{
  public:
    typedef Hello local_t;
    typedef CkIndex_Hello index_t;
    typedef CProxy_Hello proxy_t;
    typedef CProxyElement_Hello element_t;
    typedef CProxySection_Hello section_t;

    static int __idx;
    static void __register(const char *s, size_t size);
    /* DECLS: Hello(void);
     */
    // Entry point registration at startup
    
    static int reg_Hello_void();
    // Entry point index lookup
    
    inline static int idx_Hello_void() {
      static int epidx = reg_Hello_void();
      return epidx;
    }

    
    static int ckNew(void) { return idx_Hello_void(); }
    
    static void _call_Hello_void(void* impl_msg, void* impl_obj);
    
    static void _call_sdag_Hello_void(void* impl_msg, void* impl_obj);
    /* DECLS: void sayHi(int impl_noname_0);
     */
    // Entry point registration at startup
    
    static int reg_sayHi_marshall2();
    // Entry point index lookup
    
    inline static int idx_sayHi_marshall2() {
      static int epidx = reg_sayHi_marshall2();
      return epidx;
    }

    
    inline static int idx_sayHi(void (Hello::*)(int impl_noname_0) ) {
      return idx_sayHi_marshall2();
    }


    
    static int sayHi(int impl_noname_0) { return idx_sayHi_marshall2(); }
    
    static void _call_sayHi_marshall2(void* impl_msg, void* impl_obj);
    
    static void _call_sdag_sayHi_marshall2(void* impl_msg, void* impl_obj);
    
    static int _callmarshall_sayHi_marshall2(char* impl_buf, void* impl_obj_void);
    
    static void _marshallmessagepup_sayHi_marshall2(PUP::er &p,void *msg);
    /* DECLS: void sleep(int impl_noname_1);
     */
    // Entry point registration at startup
    
    static int reg_sleep_marshall3();
    // Entry point index lookup
    
    inline static int idx_sleep_marshall3() {
      static int epidx = reg_sleep_marshall3();
      return epidx;
    }

    
    inline static int idx_sleep(void (Hello::*)(int impl_noname_1) ) {
      return idx_sleep_marshall3();
    }


    
    static int sleep(int impl_noname_1) { return idx_sleep_marshall3(); }
    
    static void _call_sleep_marshall3(void* impl_msg, void* impl_obj);
    
    static void _call_sdag_sleep_marshall3(void* impl_msg, void* impl_obj);
    
    static int _callmarshall_sleep_marshall3(char* impl_buf, void* impl_obj_void);
    
    static void _marshallmessagepup_sleep_marshall3(PUP::er &p,void *msg);
    /* DECLS: Hello(CkMigrateMessage* impl_msg);
     */
    // Entry point registration at startup
    
    static int reg_Hello_CkMigrateMessage();
    // Entry point index lookup
    
    inline static int idx_Hello_CkMigrateMessage() {
      static int epidx = reg_Hello_CkMigrateMessage();
      return epidx;
    }

    
    static int ckNew(CkMigrateMessage* impl_msg) { return idx_Hello_CkMigrateMessage(); }
    
    static void _call_Hello_CkMigrateMessage(void* impl_msg, void* impl_obj);
    
    static void _call_sdag_Hello_CkMigrateMessage(void* impl_msg, void* impl_obj);
};
/* --------------- element proxy ------------------ */
 class CProxyElement_Hello : public CProxyElement_ArrayElement{
  public:
    typedef Hello local_t;
    typedef CkIndex_Hello index_t;
    typedef CProxy_Hello proxy_t;
    typedef CProxyElement_Hello element_t;
    typedef CProxySection_Hello section_t;

    CProxyElement_Hello(void) {}
    CProxyElement_Hello(const ArrayElement *e) : CProxyElement_ArrayElement(e){  }

    void ckDelegate(CkDelegateMgr *dTo,CkDelegateData *dPtr=NULL)
    {       CProxyElement_ArrayElement::ckDelegate(dTo,dPtr); }
    void ckUndelegate(void)
    {       CProxyElement_ArrayElement::ckUndelegate(); }
    void pup(PUP::er &p)
    {       CProxyElement_ArrayElement::pup(p); }

    int ckIsDelegated(void) const
    { return CProxyElement_ArrayElement::ckIsDelegated(); }
    inline CkDelegateMgr *ckDelegatedTo(void) const
    { return CProxyElement_ArrayElement::ckDelegatedTo(); }
    inline CkDelegateData *ckDelegatedPtr(void) const
    { return CProxyElement_ArrayElement::ckDelegatedPtr(); }
    CkGroupID ckDelegatedIdx(void) const
    { return CProxyElement_ArrayElement::ckDelegatedIdx(); }

    inline void ckCheck(void) const
    { CProxyElement_ArrayElement::ckCheck(); }
    inline operator CkArrayID () const
    { return ckGetArrayID(); }
    inline CkArrayID ckGetArrayID(void) const
    { return CProxyElement_ArrayElement::ckGetArrayID(); }
    inline CkArray *ckLocalBranch(void) const
    { return CProxyElement_ArrayElement::ckLocalBranch(); }
    inline CkLocMgr *ckLocMgr(void) const
    { return CProxyElement_ArrayElement::ckLocMgr(); }

    inline static CkArrayID ckCreateEmptyArray(void)
    { return CProxyElement_ArrayElement::ckCreateEmptyArray(); }
    inline static CkArrayID ckCreateArray(CkArrayMessage *m,int ctor,const CkArrayOptions &opts)
    { return CProxyElement_ArrayElement::ckCreateArray(m,ctor,opts); }
    inline void ckInsertIdx(CkArrayMessage *m,int ctor,int onPe,const CkArrayIndex &idx)
    { CProxyElement_ArrayElement::ckInsertIdx(m,ctor,onPe,idx); }
    inline void doneInserting(void)
    { CProxyElement_ArrayElement::doneInserting(); }

    inline void ckBroadcast(CkArrayMessage *m, int ep, int opts=0) const
    { CProxyElement_ArrayElement::ckBroadcast(m,ep,opts); }
    inline void setReductionClient(CkReductionClientFn fn,void *param=NULL) const
    { CProxyElement_ArrayElement::setReductionClient(fn,param); }
    inline void ckSetReductionClient(CkReductionClientFn fn,void *param=NULL) const
    { CProxyElement_ArrayElement::ckSetReductionClient(fn,param); }
    inline void ckSetReductionClient(CkCallback *cb) const
    { CProxyElement_ArrayElement::ckSetReductionClient(cb); }

    inline void ckInsert(CkArrayMessage *m,int ctor,int onPe)
    { CProxyElement_ArrayElement::ckInsert(m,ctor,onPe); }
    inline void ckSend(CkArrayMessage *m, int ep, int opts = 0) const
    { CProxyElement_ArrayElement::ckSend(m,ep,opts); }
    inline void *ckSendSync(CkArrayMessage *m, int ep) const
    { return CProxyElement_ArrayElement::ckSendSync(m,ep); }
    inline const CkArrayIndex &ckGetIndex() const
    { return CProxyElement_ArrayElement::ckGetIndex(); }

    Hello *ckLocal(void) const
    { return (Hello *)CProxyElement_ArrayElement::ckLocal(); }

    CProxyElement_Hello(const CkArrayID &aid,const CkArrayIndex1D &idx,CK_DELCTOR_PARAM)
        :CProxyElement_ArrayElement(aid,idx,CK_DELCTOR_ARGS)
    {}
    CProxyElement_Hello(const CkArrayID &aid,const CkArrayIndex1D &idx)
        :CProxyElement_ArrayElement(aid,idx)
    {}

    CProxyElement_Hello(const CkArrayID &aid,const CkArrayIndex &idx,CK_DELCTOR_PARAM)
        :CProxyElement_ArrayElement(aid,idx,CK_DELCTOR_ARGS)
    {}
    CProxyElement_Hello(const CkArrayID &aid,const CkArrayIndex &idx)
        :CProxyElement_ArrayElement(aid,idx)
    {}
/* DECLS: Hello(void);
 */
    
    void insert(int onPE=-1);
/* DECLS: void sayHi(int impl_noname_0);
 */
    
    void sayHi(int impl_noname_0, const CkEntryOptions *impl_e_opts=NULL) ;

/* DECLS: void sleep(int impl_noname_1);
 */
    
    void sleep(int impl_noname_1, const CkEntryOptions *impl_e_opts=NULL) ;

/* DECLS: Hello(CkMigrateMessage* impl_msg);
 */

};
PUPmarshall(CProxyElement_Hello)
/* ---------------- collective proxy -------------- */
 class CProxy_Hello : public CProxy_ArrayElement{
  public:
    typedef Hello local_t;
    typedef CkIndex_Hello index_t;
    typedef CProxy_Hello proxy_t;
    typedef CProxyElement_Hello element_t;
    typedef CProxySection_Hello section_t;

    CProxy_Hello(void) {}
    CProxy_Hello(const ArrayElement *e) : CProxy_ArrayElement(e){  }

    void ckDelegate(CkDelegateMgr *dTo,CkDelegateData *dPtr=NULL)
    {       CProxy_ArrayElement::ckDelegate(dTo,dPtr); }
    void ckUndelegate(void)
    {       CProxy_ArrayElement::ckUndelegate(); }
    void pup(PUP::er &p)
    {       CProxy_ArrayElement::pup(p); }

    int ckIsDelegated(void) const
    { return CProxy_ArrayElement::ckIsDelegated(); }
    inline CkDelegateMgr *ckDelegatedTo(void) const
    { return CProxy_ArrayElement::ckDelegatedTo(); }
    inline CkDelegateData *ckDelegatedPtr(void) const
    { return CProxy_ArrayElement::ckDelegatedPtr(); }
    CkGroupID ckDelegatedIdx(void) const
    { return CProxy_ArrayElement::ckDelegatedIdx(); }

    inline void ckCheck(void) const
    { CProxy_ArrayElement::ckCheck(); }
    inline operator CkArrayID () const
    { return ckGetArrayID(); }
    inline CkArrayID ckGetArrayID(void) const
    { return CProxy_ArrayElement::ckGetArrayID(); }
    inline CkArray *ckLocalBranch(void) const
    { return CProxy_ArrayElement::ckLocalBranch(); }
    inline CkLocMgr *ckLocMgr(void) const
    { return CProxy_ArrayElement::ckLocMgr(); }

    inline static CkArrayID ckCreateEmptyArray(void)
    { return CProxy_ArrayElement::ckCreateEmptyArray(); }
    inline static CkArrayID ckCreateArray(CkArrayMessage *m,int ctor,const CkArrayOptions &opts)
    { return CProxy_ArrayElement::ckCreateArray(m,ctor,opts); }
    inline void ckInsertIdx(CkArrayMessage *m,int ctor,int onPe,const CkArrayIndex &idx)
    { CProxy_ArrayElement::ckInsertIdx(m,ctor,onPe,idx); }
    inline void doneInserting(void)
    { CProxy_ArrayElement::doneInserting(); }

    inline void ckBroadcast(CkArrayMessage *m, int ep, int opts=0) const
    { CProxy_ArrayElement::ckBroadcast(m,ep,opts); }
    inline void setReductionClient(CkReductionClientFn fn,void *param=NULL) const
    { CProxy_ArrayElement::setReductionClient(fn,param); }
    inline void ckSetReductionClient(CkReductionClientFn fn,void *param=NULL) const
    { CProxy_ArrayElement::ckSetReductionClient(fn,param); }
    inline void ckSetReductionClient(CkCallback *cb) const
    { CProxy_ArrayElement::ckSetReductionClient(cb); }

    static CkArrayID ckNew(void) { return ckCreateEmptyArray(); }
    // Generalized array indexing:
    CProxyElement_Hello operator [] (const CkArrayIndex1D &idx) const
    { return CProxyElement_Hello(ckGetArrayID(), idx, CK_DELCTOR_CALL); }
    CProxyElement_Hello operator() (const CkArrayIndex1D &idx) const
    { return CProxyElement_Hello(ckGetArrayID(), idx, CK_DELCTOR_CALL); }
    CProxyElement_Hello operator [] (int idx) const 
        {return CProxyElement_Hello(ckGetArrayID(), CkArrayIndex1D(idx), CK_DELCTOR_CALL);}
    CProxyElement_Hello operator () (int idx) const 
        {return CProxyElement_Hello(ckGetArrayID(), CkArrayIndex1D(idx), CK_DELCTOR_CALL);}
    CProxy_Hello(const CkArrayID &aid,CK_DELCTOR_PARAM) 
        :CProxy_ArrayElement(aid,CK_DELCTOR_ARGS) {}
    CProxy_Hello(const CkArrayID &aid) 
        :CProxy_ArrayElement(aid) {}
/* DECLS: Hello(void);
 */
    
    static CkArrayID ckNew(const CkArrayOptions &opts);
    static CkArrayID ckNew(const int s1);

/* DECLS: void sayHi(int impl_noname_0);
 */
    
    void sayHi(int impl_noname_0, const CkEntryOptions *impl_e_opts=NULL) ;

/* DECLS: void sleep(int impl_noname_1);
 */
    
    void sleep(int impl_noname_1, const CkEntryOptions *impl_e_opts=NULL) ;

/* DECLS: Hello(CkMigrateMessage* impl_msg);
 */

};
PUPmarshall(CProxy_Hello)
/* ---------------- section proxy -------------- */
 class CProxySection_Hello : public CProxySection_ArrayElement{
  public:
    typedef Hello local_t;
    typedef CkIndex_Hello index_t;
    typedef CProxy_Hello proxy_t;
    typedef CProxyElement_Hello element_t;
    typedef CProxySection_Hello section_t;

    CProxySection_Hello(void) {}

    void ckDelegate(CkDelegateMgr *dTo,CkDelegateData *dPtr=NULL)
    {       CProxySection_ArrayElement::ckDelegate(dTo,dPtr); }
    void ckUndelegate(void)
    {       CProxySection_ArrayElement::ckUndelegate(); }
    void pup(PUP::er &p)
    {       CProxySection_ArrayElement::pup(p); }

    int ckIsDelegated(void) const
    { return CProxySection_ArrayElement::ckIsDelegated(); }
    inline CkDelegateMgr *ckDelegatedTo(void) const
    { return CProxySection_ArrayElement::ckDelegatedTo(); }
    inline CkDelegateData *ckDelegatedPtr(void) const
    { return CProxySection_ArrayElement::ckDelegatedPtr(); }
    CkGroupID ckDelegatedIdx(void) const
    { return CProxySection_ArrayElement::ckDelegatedIdx(); }

    inline void ckCheck(void) const
    { CProxySection_ArrayElement::ckCheck(); }
    inline operator CkArrayID () const
    { return ckGetArrayID(); }
    inline CkArrayID ckGetArrayID(void) const
    { return CProxySection_ArrayElement::ckGetArrayID(); }
    inline CkArray *ckLocalBranch(void) const
    { return CProxySection_ArrayElement::ckLocalBranch(); }
    inline CkLocMgr *ckLocMgr(void) const
    { return CProxySection_ArrayElement::ckLocMgr(); }

    inline static CkArrayID ckCreateEmptyArray(void)
    { return CProxySection_ArrayElement::ckCreateEmptyArray(); }
    inline static CkArrayID ckCreateArray(CkArrayMessage *m,int ctor,const CkArrayOptions &opts)
    { return CProxySection_ArrayElement::ckCreateArray(m,ctor,opts); }
    inline void ckInsertIdx(CkArrayMessage *m,int ctor,int onPe,const CkArrayIndex &idx)
    { CProxySection_ArrayElement::ckInsertIdx(m,ctor,onPe,idx); }
    inline void doneInserting(void)
    { CProxySection_ArrayElement::doneInserting(); }

    inline void ckBroadcast(CkArrayMessage *m, int ep, int opts=0) const
    { CProxySection_ArrayElement::ckBroadcast(m,ep,opts); }
    inline void setReductionClient(CkReductionClientFn fn,void *param=NULL) const
    { CProxySection_ArrayElement::setReductionClient(fn,param); }
    inline void ckSetReductionClient(CkReductionClientFn fn,void *param=NULL) const
    { CProxySection_ArrayElement::ckSetReductionClient(fn,param); }
    inline void ckSetReductionClient(CkCallback *cb) const
    { CProxySection_ArrayElement::ckSetReductionClient(cb); }

    inline void ckSend(CkArrayMessage *m, int ep, int opts = 0)
    { CProxySection_ArrayElement::ckSend(m,ep,opts); }
    inline CkSectionInfo &ckGetSectionInfo()
    { return CProxySection_ArrayElement::ckGetSectionInfo(); }
    inline CkSectionID *ckGetSectionIDs()
    { return CProxySection_ArrayElement::ckGetSectionIDs(); }
    inline CkSectionID &ckGetSectionID()
    { return CProxySection_ArrayElement::ckGetSectionID(); }
    inline CkSectionID &ckGetSectionID(int i)
    { return CProxySection_ArrayElement::ckGetSectionID(i); }
    inline CkArrayID ckGetArrayIDn(int i) const
    { return CProxySection_ArrayElement::ckGetArrayIDn(i); } 
    inline CkArrayIndex *ckGetArrayElements() const
    { return CProxySection_ArrayElement::ckGetArrayElements(); }
    inline CkArrayIndex *ckGetArrayElements(int i) const
    { return CProxySection_ArrayElement::ckGetArrayElements(i); }
    inline int ckGetNumElements() const
    { return CProxySection_ArrayElement::ckGetNumElements(); } 
    inline int ckGetNumElements(int i) const
    { return CProxySection_ArrayElement::ckGetNumElements(i); }    // Generalized array indexing:
    CProxyElement_Hello operator [] (const CkArrayIndex1D &idx) const
        {return CProxyElement_Hello(ckGetArrayID(), idx, CK_DELCTOR_CALL);}
    CProxyElement_Hello operator() (const CkArrayIndex1D &idx) const
        {return CProxyElement_Hello(ckGetArrayID(), idx, CK_DELCTOR_CALL);}
    CProxyElement_Hello operator [] (int idx) const 
        {return CProxyElement_Hello(ckGetArrayID(), *(CkArrayIndex1D*)&ckGetArrayElements()[idx], CK_DELCTOR_CALL);}
    CProxyElement_Hello operator () (int idx) const 
        {return CProxyElement_Hello(ckGetArrayID(), *(CkArrayIndex1D*)&ckGetArrayElements()[idx], CK_DELCTOR_CALL);}
    static CkSectionID ckNew(const CkArrayID &aid, CkArrayIndex1D *elems, int nElems) {
      return CkSectionID(aid, elems, nElems);
    } 
    static CkSectionID ckNew(const CkArrayID &aid, int l, int u, int s) {
      CkVec<CkArrayIndex1D> al;
      for (int i=l; i<=u; i+=s) al.push_back(CkArrayIndex1D(i));
      return CkSectionID(aid, al.getVec(), al.size());
    } 
    CProxySection_Hello(const CkArrayID &aid, CkArrayIndex *elems, int nElems, CK_DELCTOR_PARAM) 
        :CProxySection_ArrayElement(aid,elems,nElems,CK_DELCTOR_ARGS) {}
    CProxySection_Hello(const CkArrayID &aid, CkArrayIndex *elems, int nElems) 
        :CProxySection_ArrayElement(aid,elems,nElems) {}
    CProxySection_Hello(const CkSectionID &sid)       :CProxySection_ArrayElement(sid) {}
    CProxySection_Hello(int n, const CkArrayID *aid, CkArrayIndex const * const *elems, const int *nElems, CK_DELCTOR_PARAM) 
        :CProxySection_ArrayElement(n,aid,elems,nElems,CK_DELCTOR_ARGS) {}
    CProxySection_Hello(int n, const CkArrayID *aid, CkArrayIndex const * const *elems, const int *nElems) 
        :CProxySection_ArrayElement(n,aid,elems,nElems) {}
    static CkSectionID ckNew(const CkArrayID &aid, CkArrayIndex *elems, int nElems) {
      return CkSectionID(aid, elems, nElems);
    } 
/* DECLS: Hello(void);
 */
    

/* DECLS: void sayHi(int impl_noname_0);
 */
    
    void sayHi(int impl_noname_0, const CkEntryOptions *impl_e_opts=NULL) ;

/* DECLS: void sleep(int impl_noname_1);
 */
    
    void sleep(int impl_noname_1, const CkEntryOptions *impl_e_opts=NULL) ;

/* DECLS: Hello(CkMigrateMessage* impl_msg);
 */

};
PUPmarshall(CProxySection_Hello)
#define Hello_SDAG_CODE 
typedef CBaseT1<ArrayElementT<CkIndex1D>, CProxy_Hello> CBase_Hello;

/* ---------------- method closures -------------- */
class Closure_Hello {
  public:


    struct sayHi_2_closure;


    struct sleep_3_closure;


};

extern void _registerhello(void);
#endif
